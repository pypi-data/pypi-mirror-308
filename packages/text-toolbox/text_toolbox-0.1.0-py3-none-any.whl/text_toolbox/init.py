class TextTools:
    @staticmethod
    def word_count(text: str) -> dict:
        """统计文本中的字符数、单词数和行数"""
        if not text:
            return {"chars": 0, "words": 0, "lines": 0}

        chars = len(text)
        words = len(text.split())
        lines = len(text.splitlines()) or 1

        return {
            "chars": chars,
            "words": words,
            "lines": lines
        }

    @staticmethod
    def text_summary(text: str, max_length: int = 100) -> str:
        """生成文本摘要"""
        if not text:
            return ""

        text = text.strip()
        if len(text) <= max_length:
            return text

        return text[:max_length - 3] + "..."