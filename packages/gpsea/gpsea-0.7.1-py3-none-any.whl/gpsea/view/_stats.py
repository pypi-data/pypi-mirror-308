import typing

from collections import Counter

from jinja2 import Environment, PackageLoader

from gpsea.analysis.pcats import HpoTermAnalysisResult
from gpsea.view._report import GpseaReport, HtmlGpseaReport


class MtcStatsViewer:
    """
    `MtcStatsViewer` uses a Jinja2 template to create an HTML element for showing in the Jupyter notebook
    or for writing into a standalone HTML file.
    """

    def __init__(self):
        environment = Environment(loader=(PackageLoader('gpsea.view', 'templates')))
        self._cohort_template = environment.get_template("stats.html")

    def process(
        self,
        result: HpoTermAnalysisResult,
    ) -> GpseaReport:
        """
        Create an HTML to present MTC part of the :class:`~gpsea.analysis.pcats.HpoTermAnalysisResult`.

        Use the `display(HTML(..))` functions of the IPython package.

        Args:
            result (HpoTermAnalysisResult): the result to show

        Returns:
            GpseaReport: a report that can be stored to a path or displayed in
                interactive environment such as Jupyter notebook.
        """
        assert isinstance(result, HpoTermAnalysisResult)
        context = self._prepare_context(result)
        html = self._cohort_template.render(context)
        return HtmlGpseaReport(html=html)

    @staticmethod
    def _prepare_context(
        report: HpoTermAnalysisResult,
    ) -> typing.Mapping[str, typing.Any]:
        counts = Counter()
        for result in report.mtc_filter_results:
            if result.is_filtered_out():
                counts[result.mtc_issue] += 1

        n_skipped = 0
        issue_to_count = list()
        for mtc_issue, count in sorted(
            counts.items(),
            key=lambda issue2count: (issue2count[0].code, issue2count[0].reason)
        ):
            issue_to_count.append({
                "code": mtc_issue.code,
                "reason": mtc_issue.reason,
                "count": count,
            })
            n_skipped += count

        n_all = len(report.phenotypes)
        n_tested = n_all - n_skipped

        # The following dictionary is used by the Jinja2 HTML template
        return {
            "mtc_name": report.mtc_correction,
            "hpo_mtc_filter_name": report.mtc_filter_name,
            "skipped_hpo_count": n_skipped,
            "tested_hpo_count": n_tested,
            "total_hpo_count": n_all,
            "issue_to_count": issue_to_count,
        }
