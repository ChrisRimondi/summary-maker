import unittest
from unittest.mock import patch, MagicMock
from summarize import summarize_transcription, summarize_article

class TestSummarize(unittest.TestCase):

    @patch('summarize.OpenAI')
    def test_summarize_transcription(self, MockOpenAI):
        # Mock the completion response
        mock_client = MockOpenAI.return_value
        mock_completion = MagicMock()
        mock_client.chat.completions.create.return_value = mock_completion
        mock_completion.choices[0].message = "Mocked summary for transcription"

        transcription_text = "This is a test transcription."
        result = summarize_transcription(transcription_text)

        self.assertEqual(result, "Mocked summary for transcription")

    @patch('summarize.OpenAI')
    def test_summarize_article(self, MockOpenAI):
        # Mock the completion response
        mock_client = MockOpenAI.return_value
        mock_completion = MagicMock()
        mock_client.chat.completions.create.return_value = mock_completion
        mock_completion.choices[0].message = "Mocked summary for article"

        link = "http://example.com/article"
        result = summarize_article(link)

        self.assertEqual(result, "Mocked summary for article")

if __name__ == '__main__':
    unittest.main()
