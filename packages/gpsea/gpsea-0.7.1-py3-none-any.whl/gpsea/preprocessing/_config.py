import os
import sys
import typing
import warnings

import hpotk
from hpotk.validate import (
    ValidationRunner,
    ObsoleteTermIdsValidator,
    AnnotationPropagationValidator,
    PhenotypicAbnormalityValidator,
)

from stairval.notepad import create_notepad

# pyright: reportGeneralTypeIssues=false
from google.protobuf.json_format import Parse
from phenopackets import Phenopacket
from tqdm import tqdm

from gpsea.config import get_cache_dir_path
from gpsea.model import Cohort
from gpsea.model.genome import GRCh37, GRCh38, GenomeBuild
from ._api import FunctionalAnnotator, PreprocessingValidationResult
from ._generic import DefaultImpreciseSvFunctionalAnnotator
from ._patient import CohortCreator
from ._phenopacket import PhenopacketPatientCreator, PhenopacketOntologyTermOnsetParser

from ._protein import (
    ProteinMetadataService,
    ProtCachingMetadataService,
    ProteinAnnotationCache,
)
from ._uniprot import UniprotProteinMetadataService
from ._variant import VarCachingFunctionalAnnotator, VariantAnnotationCache
from ._vep import VepFunctionalAnnotator
from ._vv import VVHgvsVariantCoordinateFinder, VVMultiCoordinateService

VALIDATION_POLICIES = {"permissive", "lenient", "strict"}


def configure_caching_cohort_creator(
    hpo: hpotk.MinimalOntology,
    genome_build: str = "GRCh38.p13",
    validation_runner: typing.Optional[ValidationRunner] = None,
    cache_dir: typing.Optional[str] = None,
    include_ontology_class_onsets: bool = True,
    variant_fallback: str = "VEP",
    timeout: float = 30.0,
) -> CohortCreator[Phenopacket]:
    """
    A convenience function for configuring a caching :class:`~gpsea.preprocessing.PhenopacketPatientCreator`.

    To create the patient creator, we need hpo-toolkit's representation of HPO. Other options are optional.

    :param hpo: a HPO instance.
    :param genome_build: name of the genome build to use, choose from `{'GRCh37.p13', 'GRCh38.p13'}`.
    :param validation_runner: an instance of the validation runner.
    :param cache_dir: path to the folder where we will cache the results fetched from the remote APIs or `None`
        if the cache location should be determined as described in :func:`~gpsea.config.get_cache_dir_path`.
        In any case, the directory will be created if it does not exist (including non-existing parents).
    :param include_ontology_class_onsets: `True` if onsets in the ontology class format 
        (e.g. `HP:0003621` for Juvenile onset) should be included (default `True`).
    :param variant_fallback: the fallback variant annotator to use if we cannot find the annotation locally.
     Choose from ``{'VEP'}`` (just one fallback implementation is available at the moment).
    :param timeout: timeout in seconds for the REST APIs
    """
    cache_dir = _configure_cache_dir(cache_dir)

    build = _configure_build(genome_build)
    validator = _setup_hpo_validator(hpo, validation_runner)
    functional_annotator = _configure_functional_annotator(
        cache_dir, variant_fallback, timeout
    )
    imprecise_sv_functional_annotator = _configure_imprecise_sv_annotator(
        build, cache_dir, timeout
    )
    hgvs_annotator = VVHgvsVariantCoordinateFinder(build)
    term_onset_parser = PhenopacketOntologyTermOnsetParser.default_parser() if include_ontology_class_onsets else None
    pc = PhenopacketPatientCreator(
        hpo=hpo,
        validator=validator,
        build=build,
        functional_annotator=functional_annotator,
        imprecise_sv_functional_annotator=imprecise_sv_functional_annotator,
        hgvs_coordinate_finder=hgvs_annotator,
        term_onset_parser=term_onset_parser,
    )

    return CohortCreator(pc)


def configure_cohort_creator(
    hpo: hpotk.MinimalOntology,
    genome_build: str = "GRCh38.p13",
    validation_runner: typing.Optional[ValidationRunner] = None,
    include_ontology_class_onsets: bool = True,
    variant_fallback: str = "VEP",
    timeout: float = 30.0,
) -> CohortCreator[Phenopacket]:
    """
    A convenience function for configuring a non-caching :class:`~gpsea.preprocessing.PhenopacketPatientCreator`.

    To create the patient creator, we need hpo-toolkit's representation of HPO. Other options are optional

    :param hpo: a HPO instance.
    :param genome_build: name of the genome build to use, choose from `{'GRCh37.p13', 'GRCh38.p13'}`.
    :param validation_runner: an instance of the validation runner.
     if the data should be cached in `.cache` folder in the current working directory.
     In any case, the directory will be created if it does not exist (including non-existing parents).
    :param include_ontology_class_onsets: `True` if onsets in the ontology class format 
        (e.g. `HP:0003621` for Juvenile onset) should be included (default `True`).
    :param variant_fallback: the fallback variant annotator to use if we cannot find the annotation locally.
     Choose from ``{'VEP'}`` (just one fallback implementation is available at the moment).
    :param timeout: timeout in seconds for the VEP API
    """
    build = _configure_build(genome_build)

    validator = _setup_hpo_validator(hpo, validation_runner)
    functional_annotator = _configure_fallback_functional(variant_fallback, timeout)
    imprecise_sv_functional_annotator = _configure_imprecise_sv_annotator(
        build,
        cache_dir=None,
        timeout=timeout,
    )
    hgvs_annotator = VVHgvsVariantCoordinateFinder(build)
    term_onset_parser = PhenopacketOntologyTermOnsetParser.default_parser() if include_ontology_class_onsets else None
    pc = PhenopacketPatientCreator(
        hpo=hpo,
        validator=validator,
        build=build,
        functional_annotator=functional_annotator,
        imprecise_sv_functional_annotator=imprecise_sv_functional_annotator,
        hgvs_coordinate_finder=hgvs_annotator,
        term_onset_parser=term_onset_parser,
    )

    return CohortCreator(pc)


def configure_protein_metadata_service(
    cache_dir: typing.Optional[str] = None,
    timeout: float = 30.0,
) -> ProteinMetadataService:
    """
    Configure default protein metadata service.

    The service will cache the responses in `cache_dir` and reach out to UNIPROT API for cache misses.

    :param cache_dir: path to the folder where we will cache the results fetched from the remote APIs or `None`
     if the data should be cached in `.gpsea_cache` folder in the current working directory.
     In any case, the directory will be created if it does not exist (including any non-existing parents).
    :param timeout: timeout in seconds for the REST APIs.
    """
    warnings.warn(
        "Use `configure_default_protein_metadata_service` instead",
        DeprecationWarning,
        stacklevel=2,
    )
    return configure_default_protein_metadata_service(
        cache_dir=cache_dir,
        timeout=timeout,
    )


def configure_default_protein_metadata_service(
    protein_source: typing.Literal["UNIPROT"] = "UNIPROT",
    cache_dir: typing.Optional[str] = None,
    timeout: float = 30.0,
) -> ProteinMetadataService:
    """
    Create default protein metadata service that will cache the protein metadata
    in current working directory under `.gpsea_cache/protein_cache`
    and reach out to UNIPROT REST API if a cache entry is missing.

    :param protein_source: a `str` with the code of the protein data sources (currently accepting just `UNIPROT`).
    :param cache_dir: path to the folder where we will cache the results fetched from the remote APIs or `None`
        if the data should be cached as described by :func:`~gpsea.config.get_cache_dir_path` function.
        In any case, the directory will be created if it does not exist (including any non-existing parents).
    :param timeout: timeout in seconds for the REST APIs.
    """
    cache_dir = _configure_cache_dir(cache_dir)
    return _configure_protein_service(
        protein_fallback=protein_source,
        cache_dir=cache_dir,
        timeout=timeout,
    )


def _configure_protein_service(
    protein_fallback: str,
    cache_dir: str,
    timeout: float,
) -> ProteinMetadataService:
    # (1) ProteinMetadataService
    # Setup fallback
    fallback_service = _configure_fallback_protein_service(
        protein_fallback,
        timeout,
    )
    # Setup protein metadata cache
    prot_cache_dir = os.path.join(cache_dir, "protein_cache")
    os.makedirs(prot_cache_dir, exist_ok=True)
    prot_cache = ProteinAnnotationCache(prot_cache_dir)
    # Assemble the final protein metadata service
    protein_metadata_service = ProtCachingMetadataService(prot_cache, fallback_service)
    return protein_metadata_service


def _configure_fallback_protein_service(
    protein_fallback: str,
    timeout: float,
) -> ProteinMetadataService:
    if protein_fallback == "UNIPROT":
        return UniprotProteinMetadataService(timeout)
    else:
        raise ValueError(f"Unknown protein fallback annotator type {protein_fallback}")


def _configure_cache_dir(
    cache_dir: typing.Optional[str] = None,
) -> str:
    cache_path = get_cache_dir_path(cache_dir)
    os.makedirs(cache_path, exist_ok=True)

    return str(cache_path)


def _configure_build(genome_build: str) -> GenomeBuild:
    if genome_build == "GRCh38.p13":
        return GRCh38
    elif genome_build == "GRCh37.p13":
        return GRCh37
    else:
        raise ValueError(
            f"Unknown build {genome_build}. Choose from ['GRCh37.p13', 'GRCh38.p13']"
        )


def _setup_hpo_validator(
    hpo: hpotk.MinimalOntology,
    validator: typing.Optional[ValidationRunner],
) -> ValidationRunner:
    if validator is None:
        # This will be the default validator
        return ValidationRunner(
            (
                ObsoleteTermIdsValidator(hpo),
                AnnotationPropagationValidator(hpo),
                PhenotypicAbnormalityValidator(hpo),
            )
        )
    else:
        return hpotk.util.validate_instance(validator, ValidationRunner, "validator")


def _configure_functional_annotator(
    cache_dir: str,
    variant_fallback: str,
    timeout: float,
) -> FunctionalAnnotator:

    # (2) FunctionalAnnotator
    # Setup fallback
    fallback = _configure_fallback_functional(variant_fallback, timeout)

    # Setup variant cache
    var_cache_dir = os.path.join(cache_dir, "variant_cache")
    os.makedirs(var_cache_dir, exist_ok=True)
    var_cache = VariantAnnotationCache(var_cache_dir)

    # Assemble the final functional annotator
    return VarCachingFunctionalAnnotator(var_cache, fallback)


def _configure_fallback_functional(
    variant_fallback: str,
    timeout: float,
) -> FunctionalAnnotator:
    if variant_fallback == "VEP":
        fallback = VepFunctionalAnnotator(timeout=timeout)
    else:
        raise ValueError(f"Unknown variant fallback annotator type {variant_fallback}")
    return fallback


def _configure_imprecise_sv_annotator(
    genome_build: GenomeBuild,
    cache_dir: typing.Optional[str] = None,
    timeout: float = 30.0,
):
    # Setup cache for SVs
    if cache_dir is not None:
        sv_cache_dir = os.path.join(cache_dir, "sv_cache")
        # TODO: implement the cache.
        # os.makedirs(sv_cache_dir, exist_ok=True)
        # var_cache = VariantAnnotationCache(sv_cache_dir)

    return DefaultImpreciseSvFunctionalAnnotator(
        gene_coordinate_service=VVMultiCoordinateService(
            genome_build=genome_build,
            timeout=timeout,
        )
    )


def load_phenopacket_folder(
    pp_directory: str,
    cohort_creator: CohortCreator[Phenopacket],
    validation_policy: typing.Literal["permissive", "lenient", "strict"] = "permissive",
) -> typing.Tuple[Cohort, PreprocessingValidationResult]:
    """
    Load phenopacket JSON files from a directory, validate the patient data, and assemble the patients into a cohort.

    A file with `.json` suffix is considered to be a JSON file and all JSON files are assumed to be phenopackets.
    Non-JSON files are ignored.

    :param pp_directory: path to a folder with phenopacket JSON files. An error is raised if the path does not point to
      a directory with at least one phenopacket.
    :param cohort_creator: cohort creator for turning a sequence of phenopacket
      into a :class:`~gpsea.model.Cohort`.
    :param validation_policy: a `str` with the validation policy.
      The value must be one of `{'permissive', 'lenient', 'strict'}`
    :return: a tuple with the cohort and the validation result.
    """
    # Load phenopackets
    pp_files = _find_phenopacket_files(pp_directory)

    # Map to patients
    return load_phenopacket_files(
        pp_files=pp_files,
        cohort_creator=cohort_creator,
        validation_policy=validation_policy,
    )


def load_phenopacket_files(
    pp_files: typing.Iterator[str],
    cohort_creator: CohortCreator[Phenopacket],
    validation_policy: typing.Literal["permissive", "lenient", "strict"] = "permissive",
) -> typing.Tuple[Cohort, PreprocessingValidationResult]:
    """
    Load phenopacket JSON files, validate the data, and assemble into a :class:`~gpsea.model.Cohort`.

    Phenopackets are validated, assembled into a cohort, and the validation results are reported back.

    :param pp_files: an iterator with paths to phenopacket JSON files.
    :param cohort_creator: cohort creator for turning a phenopacket collection
      into a :class:`~gpsea.model.Cohort`.
    :param validation_policy: a `str` with the validation policy.
      The value must be one of `{'permissive', 'lenient', 'strict'}`
    :return: a tuple with the cohort and the validation result.
    """
    return load_phenopackets(
        phenopackets=(_load_phenopacket(pp_file) for pp_file in pp_files),
        cohort_creator=cohort_creator,
        validation_policy=validation_policy,
    )


def load_phenopackets(
    phenopackets: typing.Iterable[Phenopacket],
    cohort_creator: CohortCreator[Phenopacket],
    validation_policy: typing.Literal["permissive", "lenient", "strict"] = "permissive",
) -> typing.Tuple[Cohort, PreprocessingValidationResult]:
    """
    Validate the phenopackets and assemble into a :class:`~gpsea.model.Cohort`.

    The results of the validation are reported back.

    :param phenopackets: path to a folder with phenopacket JSON files. An error is raised if the path does not point to
      a directory with at least one phenopacket.
    :param cohort_creator: cohort creator for turning a sequence of phenopacket
      into a :class:`~gpsea.model.Cohort`.
    :param validation_policy: a `str` with the validation policy.
      The value must be one of `{'permissive', 'lenient', 'strict'}`
    :return: a tuple with the cohort and the validation result.
    """
    # Check inputs before doing anything
    hpotk.util.validate_instance(cohort_creator, CohortCreator, "cohort_creator")
    if validation_policy.lower() not in VALIDATION_POLICIES:
        raise ValueError(f"{validation_policy} must be one of {VALIDATION_POLICIES}")

    # Turn phenopackets into a cohort using the cohort creator.
    # Keep track of the progress by wrapping the list of phenopackets
    # with TQDM 😎
    cohort_iter = tqdm(
        phenopackets, desc="Individuals Processed", file=sys.stdout, unit="individuals"
    )
    notepad = create_notepad(label="Phenopackets")
    cohort = cohort_creator.process(cohort_iter, notepad)

    validation_result = PreprocessingValidationResult(
        policy=validation_policy,
        notepad=notepad,
    )

    return cohort, validation_result


def _find_phenopacket_files(
    pp_dir: str,
) -> typing.Iterator[str]:
    fpath_pp_abs = os.path.abspath(pp_dir)
    if not os.path.isdir(fpath_pp_abs):
        raise ValueError(f"`{fpath_pp_abs}` does not point to a directory")

    for patient_file in os.listdir(pp_dir):
        if patient_file.endswith(".json"):
            yield os.path.join(pp_dir, patient_file)


def _load_phenopacket(phenopacket_path: str) -> Phenopacket:
    """
    Load phenopacket JSON file.

    :param phenopacket_path: a `str` pointing to phenopacket JSON file.
    """
    with open(phenopacket_path) as f:
        return Parse(f.read(), Phenopacket())
