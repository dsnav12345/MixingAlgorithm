# Usage
## Single test case execution
1. Comment the part **Input from command line argument** and un comment the part **Manual input**
2. Provide the input in inp array in the format mentioned
    1. cRASS => inp = [m, d, r, concentraions, target concentration, m^d]
    2. vRASS => inp = [m, d, r, concentrations, costs, target concentration, m^d]
3. Comment the line under the comment **Redirect output to the file**
4. Run the file
5. Wait for the output to be printed

## Simulation
1. Comment the **Manual input** part and uncomment **Input from command line argument** part
2. Uncomment the line below the comment **Redirect output to the file**
3. Make sure the **outputs** folder is empty and is in the same location this file present
4. Make sure the **inputs** folder is in the same location this file is present
5. Make sure the **script.sh** file is in the same location this file is present
6. Open the terminal into this location and run the following command
    > $ bash script.sh
7. This will take nearly 4-5 days to complete the simulation and results will be in the files in the **output** directory

### Plotting graphs
1. Run the **plot.py** file and make sure the **Plots** folder is in same location
2. All the plots will be in the **Plots** directory