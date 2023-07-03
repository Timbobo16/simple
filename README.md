<!-- TABLE OF CONTENTS -->

  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#tutorial">Tutorial</a></li>
      <ul>
        <li><a href="#prerequisites">Quickstart</a></li>
        <li><a href="#prerequisites">Tensorboard</a></li>
      </ul>
    </li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>



<br>

---
<!-- GETTING STARTED -->

## Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

The UCI engine component will only work on Windows.

The SIMPLE library requires Docker:
Install [Docker](https://github.com/davidADSP/SIMPLE/issues) and [Docker Compose](https://docs.docker.com/compose/install/) to make use of the `docker-compose.yml` file

### Installation

For the UCI engine:

1. The engine is dist/cppo.exe

For the SIMPLE program:

1. Clone the repo and cd into SIMPLE

2. Build the image and 'up' the container.
   ```sh
   docker-compose up -d
   ```
3. Choose an environment to install in the container (`tictactoe`, `connect4`, `sushigo`, `geschenkt`, `butterfly`, and `connect5`(chess) are implemented)
   ```sh
   bash ./scripts/install_env.sh connect5
   ```

---
<!-- TUTORIAL -->
## Tutorial

This is a quick tutorial to allow you to start using the two entrypoints into the SIMPLE library: `test.py` and `train.py`.

---
<!-- QUICKSTART -->
### Quickstart

#### `test.py`

This entrypoint allows you to play against a trained AI, pit two AIs against eachother or play against a baseline random model.

For example, try the following command to play against a baseline random model in the chess (sorry I called it connect5) environment.
   ```sh
   docker-compose exec app python3 test.py -d -g 1 -a base human -e connect5
   ```

#### `train.py`

This entrypoint allows you to start training the AI using selfplay PPO. The underlying PPO engine is from the [Stable Baselines](https://stable-baselines.readthedocs.io/en/master/) package.


In order to train the existing best model, you can drop the `-r` reset flag from the `train.py` entrypoint arguments - it will just pick up from where it left off.

   ```sh
   docker-compose exec app python3 train.py -e connect5
   ```


In order to delete all old models train the agent to learn how to play chess from scratch, run the following command (WARNING: this will delete all the old chess models):
   ```sh
   docker-compose exec app python3 train.py -r -e connect5
   ```

After a lot of iterations the process should have achieved above the default threshold score of 0.2 and will output a new `best_model.zip` to the `/zoo/connect5` folder.

Training runs until you kill the process manually (e.g. with Ctrl-C), so do that now.

You can now use the `test.py` entrypoint to play 100 games silently between the current `best_model.zip` and the random baselines model as follows:

  ```sh
  docker-compose exec app python3 test.py -g 100 -a best_model base -e connect5
  ```

---
<!-- TENSORBOARD -->
### Tensorboard

To monitor training, you can start Tensorboard with the following command:

  ```sh
  bash scripts/tensorboard.sh
  ```

Navigate to `localhost:6006` in a browser to view the output.

In the `/zoo/pretrained/` folder there is a pre-trained `/<game>/best_model.zip` for each game (besides chess, that one is in `/zoo/connect5`), that can be copied up a directory (e.g. to `/zoo/sushigo/best_model.zip`) if you want to test playing against a pre-trained agent right away.




---
<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements

One repository that deserves particular acknowledgement is David Foster's SIMPLE library.
This is what I used for the PPO.

* [davidADSP - SIMPLE](https://github.com/davidADSP/SIMPLE)
