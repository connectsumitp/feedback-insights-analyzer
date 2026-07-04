from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))

import pandas as pd

from utils import classify_sentiment, detect_themes, prepare_feedback, theme_summary


def run_smoke_tests():
    assert classify_sentiment("This is excellent and very easy to use")[0] == "Positive"
    assert classify_sentiment("Payment failed and support is not responding")[0] == "Negative"

    themes = detect_themes("My payment failed and customer support did not respond.")
    assert "Payment" in themes
    assert "Support" in themes

    data = pd.DataFrame(
        {
            "feedback": [
                "Payment failed and customer support did not respond.",
                "The app is easy and reliable.",
                "Leads are irrelevant for my business.",
            ],
            "rating": [1, 5, 2],
        }
    )
    processed = prepare_feedback(data)
    summary = theme_summary(processed)
    assert len(processed) == 3
    assert not summary.empty
    print("Smoke tests passed.")


if __name__ == "__main__":
    run_smoke_tests()
