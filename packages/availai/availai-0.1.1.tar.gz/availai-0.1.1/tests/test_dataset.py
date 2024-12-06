from availai.dataset import Dataset

def main():
    project = 'football_players'
    project = 'football-players-detection'

    dataset = Dataset(path='./datasets/football-players-detection.v12i.yolov8',
                      name='football-players-detection.v12i.yolov8',
                      project_name=project,
                      wandb_api_key='./wandb_api_key.txt')
    # dataset.create_wandb_artifact()
    dataset.log_table_on_wandb()

if __name__ == '__main__':
    main()