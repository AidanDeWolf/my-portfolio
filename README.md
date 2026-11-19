# my-portfolio

# NFL Defensive Analytics Dashboard

## Project Description
This project is an interactive Streamlit application that explores NFL defensive performance from the 2024 season through Week 10 of the 2026 season. It uses statistical visualizations and interactive filters to examine how defensive metrics such as pressures, sacks, interceptions, and takeaways relate to team game outcomes.

## Author
**Aidan DeWolf**

## App Navigation

The application contains four pages:

- **Bio:** Introduction and background information.
- **EDA Gallery:** Exploratory visualizations examining relationships between defensive statistics and game outcomes.
- **Dashboard:** Interactive dashboard with team selection, date ranges, defensive statistic filters, win percentages, and game outcome comparisons.
- **Future Work:** Potential project improvements and reflection on the development process.

## Dataset Information

**Dataset:** NFL Team Defense Games 2024 Week 1 Through 2026 Week 10

**Source:** [Stathead Team Game Stats Finder](https://www.sports-reference.com/stathead/football/team-game-finder.cgi)

- **Number of records:** 1,388 team-game observations.
- **Unit of observation:** One team's defensive performance in one regular-season game.
- **Time period:** 2024 season through Week 10 of the 2026 season.

### Data Preprocessing

The following preprocessing was performed:

Converted game dates into datetime format.

Created a Pressure Rate variable by dividing pressures by defensive plays.

Created a Result variable categorizing each game as a win, tie, or loss.

Created a numerical Win variable, where 1 represents a win, 0.5 represents a tie, and 0 represents a loss.

Created a Fumbles Recovered stat, using Takeaways and Interceptions to find it

Used existing defensive statistics to examine relationships with opponent points and game outcomes.

Ethics Note

This dataset contains professional NFL team and game statistics rather than personal or sensitive individual-level information.

Requirements

See requirements.txt for the Python dependencies required to run the application.

Running Locally

Clone the repository:

git clone https://github.com/AidanDeWolf/my-portfolio

Navigate into the project directory:

cd my-portfolio

Install dependencies:

pip install -r requirements.txt

Start the Streamlit application:

streamlit run app.py

Screenshots

Screenshots of the application can be added here to preview the Bio, EDA Gallery, and Dashboard pages.

AI Assistance Acknowledgment

ChatGPT was used to assist with Python debugging, Streamlit development, and documentation. All project decisions, data analysis, and final implementation were reviewed by the author.
