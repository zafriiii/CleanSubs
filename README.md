# CleanSubs

CleanSubs is a Windows desktop application that scans subtitle (.srt) files for profanity words based on Malaysian regulations. It is designed for content creators, broadcasters, and media producers who need to ensure their content complies with local censorship guidelines.

## Features

- **Subtitle Scanning:**  
  Scans one or more `.srt` files for profane words.

- **Classification Levels:**  
  Choose from three classification levels (U, P12 & 13, and 16 & 18) based on the severity of profanities defined under Malaysian regulation.

- **Movie Start Time Adjustment:**  
  Enter the movie's starting time in 24-hour `HH:MM:SS` format. The application calculates and displays the exact time when each profanity appears.

- **Clear and Formatted Output:**  
  Flagged subtitle entries are numbered and show a bolded timestamp (e.g., `1. At 20:08:09:`) followed by the offending subtitle block.

## Requirements

- Windows 10/11

## Installation

1. Go to the [Releases](Releases) tab of this repository.
2. Download the **CleanSubsSetup.exe** file provided in the latest release.
3. Install CleanSubs by clicking **CleanSubsSetup.exe** and follow the installation instruction.
4. Run `CleanSubs.exe`.

## Usage

1. **Select Subtitle Files:**  
   Click the **Select SRT Files** button and choose one or more `.srt` files to scan.

3. **Choose Classification:**  
   Select the desired classification level from the dropdown:
   - **U**
   - **P12 & 13**
   - **16 & 18**

4. **Enter Movie Starting Time:**  
   Input the movie's starting time in `HH:MM:SS` format (24-hour clock).

5. **Scan for Profanities:**  
   Click the **Scan** button.  
   The application will display a numbered list of flagged entries along with the exact (adjusted) times when the profanities occur.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
