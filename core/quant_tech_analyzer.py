# =======================================================================================================================
# QStudio - quant_tech_analyzer.py
# (c) Alberto Sfolcini <a.sfolcini@gmail.com>
# www.surprisalx.com
# =======================================================================================================================
import requests
import pandas as pd
import numpy as np
import json
import os
from core.Datahub import Datahub
import core.config as cfg

class QuantTechAnalyzer:

    def __init__(self):
        # Load configuration from file
        config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "qstudio-configuration.json")
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        self.api_url = config.get(
            "LLM_API_URL",
            "https://test-cx-api.giorgioarmani.tech/_v1/llm/proxy/v1/chat/completions"
        )

        self.api_key = config.get("LLM_API_KEY")
        self.model = config.get("LLM_MODEL", "qwen")

        if not self.api_key:
            raise ValueError("Missing LLM_API_KEY in configuration file")

    # =========================
    # FEATURES
    # =========================
    def compute_features(self, df: pd.DataFrame) -> dict:

        # Convert 'Close' to 'close' if needed
        close_col = 'close'
        if 'close' not in df.columns and 'Close' in df.columns:
            close_col = 'Close'
            
        close = df[close_col]

        ret_1d = close.pct_change().iloc[-1]
        ret_5d = close.pct_change(5).iloc[-1]

        sma20 = close.rolling(20).mean().iloc[-1]
        sma50 = close.rolling(50).mean().iloc[-1]

        delta = close.diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / (loss + 1e-9)
        rsi = 100 - (100 / (1 + rs))

        vol = close.pct_change().rolling(20).std().iloc[-1]

        price = close.iloc[-1]

        return {
            "last_price": float(price),
            "ret_1d": float(ret_1d),
            "ret_5d": float(ret_5d),
            "rsi": float(rsi.iloc[-1]),
            "volatility": float(vol),
            "sma20": float(sma20),
            "sma50": float(sma50),
            "trend": "bullish" if sma20 > sma50 else "bearish",
        }

    # =========================
    # PROMPT
    # =========================
    def build_prompt(self, ticker: str, features: dict) -> str:

        return f"""You are a hedge fund equity analyst.

Analyze {ticker} using DAILY technical data.

DATA:
{json.dumps(features, indent=2)}

Return:

1. Market Regime
2. Momentum
3. Volatility
4. Structure
5. Trading Plan
6. Final Bias (one of: STRONG LONG / LONG / WEAK LONG / NEUTRAL / WEAK SHORT / SHORT / STRONG SHORT)

Be concise and actionable."""

    # =========================
    # LLM CALL (YOUR ENDPOINT)
    # =========================
    def call_llm(self, prompt: str) -> str:

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a hedge fund analyst."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2
        }

        res = requests.post(self.api_url, headers=headers, json=payload)

        if res.status_code != 200:
            raise Exception(res.text)

        return res.json()["choices"][0]["message"]["content"]

    # =========================
    # SCORE
    # =========================
    def compute_score(self, f: dict) -> float:

        score = 0

        score += 1 if f["trend"] == "bullish" else -1

        if f["rsi"] > 70:
            score -= 0.5
        elif f["rsi"] < 30:
            score += 0.5

        score += 0.5 if f["ret_5d"] > 0 else -0.5

        if f["volatility"] > 0.03:
            score -= 0.5

        return float(score)


    # =========================
    # SINGLE TICKER
    # =========================
    def analyze(self, ticker: str, df: pd.DataFrame) -> dict:

        features = self.compute_features(df)
        features["quant_score"] = self.compute_score(features)

        prompt = self.build_prompt(ticker, features)
        llm_output = self.call_llm(prompt)

        return {
            "ticker": ticker,
            "features": features,
            "llm_report": llm_output
        }