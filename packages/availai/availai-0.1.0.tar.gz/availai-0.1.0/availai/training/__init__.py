import wandb
from ultralytics import YOLO


class YoloTrainer:
    def __init__(self, model_name, project_name, config, save_dir="models/"):
        """
        Initialize the YoloTrainer class with the given parameters.

        Parameters:
        - model_name: str, the model type (e.g., 'yolov8s')
        - project_name: str, the WandB project name for logging.
        - config: dict, configurations like epochs, batch_size, data path, etc.
        - save_dir: str, directory to save trained models.
        """
        self.model_name = model_name
        self.project_name = project_name
        self.config = config
        self.save_dir = save_dir
        self.model = YOLO(model_name)

        # Initialize WandB
        wandb.init(project=self.project_name, config=self.config)

    def train(self):
        """
        Train the YOLO model with the specified configuration.
        Logs the progress to WandB and saves model checkpoints.
        """
        # Run training and log to WandB
        train_results = self.model.train(
            data=self.config['data'],
            epochs=self.config['epochs'],
            batch_size=self.config['batch_size'],
            save_dir=self.save_dir,
            project=self.project_name,
            name=self.config.get("experiment_name", "default_run"),
            save_period=self.config.get("save_period", 1)
        )

        # Log metrics and other details to WandB
        wandb.log({"train_results": train_results})

        # Save model checkpoint
        self.model.save(f"{self.save_dir}/{self.config.get('experiment_name', 'model_checkpoint.pt')}")

    def evaluate(self):
        """
        Evaluate the YOLO model on the validation or test dataset.
        Logs the evaluation results to WandB.
        """
        eval_results = self.model.val(data=self.config['data'])

        # Log evaluation results
        wandb.log({"eval_results": eval_results})

        return eval_results

    def finish(self):
        """
        Finalize WandB logging session.
        """
        wandb.finish()
