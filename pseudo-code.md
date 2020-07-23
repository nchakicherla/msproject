- User inputs: 
  - Number of strips - N
  - Time required to load strips onto belt - L
  - Number of images per strips - I
  - Number of minutes/seconds between each image - T
  - Number of lighting colors and brightness needed for each strip (predefined profiles in .txt file) - P
  - Whether or not images are captured when reaction is initiated - F
  - 
- Obtain user inputs, and wait for push button input



- Initial loading loop allows for initiating reaction separately, and placing strips onto belt
  - For each strip (N)
    - User initiates reaction before placing on conveyor belt
    - Images are captured at reaction start in lighting conditions if specified by F (nested loop) 
    - Motor rotates suitable amount to allow for initiation of reaction on new strip
      - Time is determined by dividing time for 360 degree rotation by number of strips, specified by N
      - Also needs to consider time required to apply reagents to strips, determined by user technique
    - Motor pauses for suitable amount of time to allow for loading, specified by L
    - End of loop should mean that first strip is back in viewfinder
- Depending on how much time has elapsed during loading loop, a certain amount of time is elapsed depending on T
  - Once T has elapsed in total, additional reaction images are obtained
- For each (I - 1)
  - Take pictures in lighting specified lighting conditions (nested loop)
    - Set lighting depending on P
    - Take and save picture
  - Rotate belt until next strip is in viewfinder, depending on N
    
- **Additional Features**
  - Allow irregular photography, for example 2 images separated by 3 minutes, followed by 4 images every 1 or 2 minutes, etc.
  - Allow for more time between strips, for example if reagent is not prepared in advance
  - Allow for self calibration, meaning number of strips does not have to be specified and different strips can have different image timing (not required)