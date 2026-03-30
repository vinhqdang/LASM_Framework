import json

class ReportingUtils:
    @staticmethod
    def to_json(data: dict, file_path: str):
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
            
    @staticmethod
    def to_latex(report_data: dict, file_path: str):
        """Simplistic placeholder to generate a LaTeX table string from dict."""
        tex = "\\begin{table}[]\n\\centering\n\\begin{tabular}{|l|c|}\n\\hline\nMetric & Value \\\\\n\\hline\n"
        for k, v in report_data.items():
            if isinstance(v, float):
                tex += f"{k} & {v:.3f} \\\\\n"
            else:
                tex += f"{k} & {v} \\\\\n"
        tex += "\\hline\n\\end{tabular}\n\\end{table}"
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(tex)
