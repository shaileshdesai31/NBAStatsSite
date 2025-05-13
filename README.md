# 🏀 NBAStatsSite

NBAStatsSite is a Flask-based web application that allows users to explore advanced NBA player stats with contextual filters. It’s built to help identify how players perform under different game conditions and against specific types of opponents.

## 📊 Features

- User login with email and password (hashed using `werkzeug.security`)
- Search NBA players and filter their performances; some examples:
  - Home vs. Away games
  - Opponents with Top N Defensive Rating
  - Opponents with Top N Pace
  - Opponents with Bottom N Offensive Rating
  - Opponents with a win % of N or better
- Data is pulled from the **NBA API** and **Basketball Reference**

## 🧰 Tech Stack

- **Backend**: Python, Flask
- **Database**: SQL (via SQLAlchemy)
- **Auth**: Werkzeug security
- **Data Sources**: NBA API, Basketball Reference

## 🛠️ Setup Instructions

1. Clone this repository.
2. Set up the database by following the instructions in the [NBA_BoxScores](https://github.com/shaileshdesai31/NBA_BoxScores) repository.
3. Create a `User` table with:
   - `email`
   - `password` (hashed with `werkzeug.security`)
4. Update your `DB_URI` with your actual credentials in the base_structure.py file.
   - It's recommended to make your DB_URI an env variable
5. To run locally, run main.py
   - If running on a cloud server, setup the site to run using Apache

## Credits
- Autocomplete used is implemented from https://github.com/devbridge/jQuery-Autocomplete
- Code written and all contextual functionality by Shailesh Desai with use of base flask structure
