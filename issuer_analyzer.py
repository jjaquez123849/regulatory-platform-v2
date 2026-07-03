import re

from app.engines.document_intelligence.analyzers.base_analyzer import BaseAnalyzer


class IssuerAnalyzer(BaseAnalyzer):

    REGULATORS = [
        "superintendencia de bancos",
        "superintendencia del mercado de valores",
        "uaf",
        "dgii",
        "pro consumidor",
        "ministerio público",
        "fiscalía",
    ]

    def analyze(
        self,
        text,
        understanding
    ):

        lower = text.lower()

        for regulator in self.REGULATORS:

            if regulator in lower:

                understanding.regulator = regulator.title()

                understanding.issuer = regulator.title()

                return

        patterns = [
            r"de:\s*(.+)",
            r"emitido por:\s*(.+)",
            r"remitente:\s*(.+)"
        ]

        for pattern in patterns:

            match = re.search(
                pattern,
                text,
                re.IGNORECASE
            )

            if match:

                understanding.issuer = match.group(1).strip()

                return
