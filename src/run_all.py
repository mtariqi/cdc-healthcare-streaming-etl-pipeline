from main import run_pipeline
from bi_dashboard import generate_bi_summary
from monitoring import run_public_health_monitoring
from ml_model import train_health_indicator_model


if __name__ == "__main__":
    run_pipeline(limit=1000)
    generate_bi_summary()
    run_public_health_monitoring(threshold=30.0)
    train_health_indicator_model()
