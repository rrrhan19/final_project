"""在 held-out 測試集上評估偵測模型（顧問 eval-designer 建議）。

重點：用『沒參與訓練』的 testset.jsonl 報 Precision / Recall / F1 + confusion matrix，
特別呈現 scam-class Recall（漏報=放走詐騙）與 legit 的 False Positive Rate（誤報=正常被當詐騙）。
⚠️ 絕不引用 train.py 的訓練集準確率（那會因小資料過擬合而接近 100%，毫無意義）。

    cd backend-api && python -m model.evaluate
"""
from __future__ import annotations

import json
from pathlib import Path

TESTSET = Path(__file__).resolve().parent / "testset.jsonl"


def main() -> None:
    import joblib
    from sklearn.metrics import classification_report, confusion_matrix

    model_path = Path(__file__).resolve().parent / "scam_clf.joblib"
    if not model_path.exists():
        print("找不到模型，請先 python -m model.train")
        return
    clf = joblib.load(model_path)

    rows = [json.loads(l) for l in TESTSET.read_text(encoding="utf-8").splitlines() if l.strip()]
    texts = [r["text"] for r in rows]
    y_true = [1 if r["label"] == "scam" else 0 for r in rows]
    y_pred = [int(p >= 0.5) for p in clf.predict_proba(texts)[:, 1]]

    n_scam = sum(y_true)
    n_legit = len(y_true) - n_scam
    print(f"=== Held-out 測試集評估（{len(rows)} 筆：詐騙 {n_scam} / 正常 {n_legit}）===\n")
    print(classification_report(y_true, y_pred, target_names=["正常 legit", "詐騙 scam"], digits=3, zero_division=0))

    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    print("混淆矩陣：")
    print(f"  實際詐騙→判詐騙(TP)={tp}  實際詐騙→判正常(FN, 漏報)={fn}")
    print(f"  實際正常→判詐騙(FP, 誤報)={fp}  實際正常→判正常(TN)={tn}")
    recall = tp / (tp + fn) if (tp + fn) else 0
    fpr = fp / (fp + tn) if (fp + tn) else 0
    print(f"\n重點指標（裸模型）：")
    print(f"  詐騙偵出率 Recall（越高越好，漏報越少）= {recall:.1%}")
    print(f"  正常誤報率 FPR（越低越好，別把正常當詐騙）= {fpr:.1%}")

    # === 實際產品的 ensemble（model + 規則 + RAG）表現 ===
    from app.detect import detect

    ens_pred = []
    for t in texts:
        v = detect(t)["verdict"]
        ens_pred.append(1 if v == "scam" else 0)  # legit/uncertain 視為未標詐騙
    etn, efp, efn, etp = confusion_matrix(y_true, ens_pred, labels=[0, 1]).ravel()
    erecall = etp / (etp + efn) if (etp + efn) else 0
    efpr = efp / (efp + etn) if (efp + etn) else 0
    print(f"\n重點指標（實際 ensemble = model+規則+RAG，產品真正用的）：")
    print(f"  詐騙偵出率 Recall = {erecall:.1%}（uncertain 視為未判詐騙，故偏保守）")
    print(f"  正常誤報率 FPR   = {efpr:.1%}")
    print("\n註：測試集為人工標註、與訓練資料不重疊；樣本量小，結論僅供專題參考。")


if __name__ == "__main__":
    main()
