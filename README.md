# 3D Hand Tracking Using Mediapipe and Unity

In this repo I used [Mediapipe](https://github.com/google-ai-edge/mediapipe) package for extracting landmark from a hand and then I send these landmarks data to the [Unity](https://github.com/Unity-Technologies) using socket and then I show the landmarks and their connections.

## How to install

### Run this command

```bash
pip install -r requirements.txt
```

Then you need to install `Unity`. You can download and install it from [here](https://docs.unity3d.com/hub/manual/InstallHub.html).

## How to run

#### First you need to copy my `Assets` folder into your `Unity` project instead of your `Assets` folder

#### Then you need to run your `Unity` project

#### Then you can run the AI using the following command

```bash
clear; python main.py
```

#### You can also see the other arguments of it with this command

```bash
clear; python main.py --help
```

*For Example:*

- *`--webcam`*: You can change your webcam ID. **default:***`0`*
- *`--min-conf`*: You can change the minimum number of confidence for hand detection. **default:***`.7`*
- *`--min-track-conf`*: You can change the minimum number of confidence for hand tracking. **default:***`.8`*
- *`--ip`*: You can change the IP address to send data to Unity and C#. **default:***`127.0.0.1`*
- *`--port`*: You can change the port to send data to Unity and C#. **default:***`5052`*

### Result

![Result](./out/3d_hand_tracking_854x480.gif)