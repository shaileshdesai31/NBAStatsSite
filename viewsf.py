from flask import Blueprint, render_template, request, flash, redirect, url_for, Response, jsonify
from flask_login import login_required, current_user
from sqlalchemy.sql import text
from matplotlib.figure import Figure
import pandas as pd
import datetime
from base_structure import db
import base64
from io import BytesIO
import json
import matplotlib.dates as mdates

views = Blueprint('views', __name__)


@views.route('/', methods=['GET'])
@login_required
def home():
    conn = db.engine

    """q = SELECT pl.player_name, (select pl1.team from PlayerLog pl1 where pl1.player_name = pl.player_name order by pl1.game_id desc limit 1) as team, round(avg(pl.sp/60),2) `min`, round(avg(pl.pts),2) pts, round(avg(pl.pts+pl.ast+pl.orb+pl.drb),2) `p+r+a`, round(avg(pl.ast),2) ast, round(avg(pl.orb+pl.drb),2) reb, round(avg(pl.blk),2) blk, round(avg(pl.stl),2) stl, round(avg(pl.tov),2) tov, round(100*sum(pl.fg)/sum(pl.fga),2) `fg%`, round(100*sum(pl.ft)/sum(pl.fta),2) `ft%`, round(100*sum(pl.tp)/sum(pl.tpa),2) `3p%`, count(*) gp
            from PlayerLog pl
            join Game g on g.game_id = pl.game_id
            join Standings s on pl.opp = s.team and s.season = 2024
            join team_advanced_stats tas on tas.team = pl.opp
            where g.season = 2024
            group by pl.player_name, 2
            order by 4 desc
            limit 20;
    q = text(q)
    df = pd.read_sql(q, conn, index_col=None)"""

    return render_template("home.html", user=current_user)


@views.route('/psearch', methods=['GET', 'POST'])
@login_required
def psearch():
    if request.method == "POST":
        player1 = request.form.get('player1')
        stat = request.form.get('stat')
        base = request.form.get('base')
        d = request.form.get('d')
        opp_def = request.form.get('opp_def')
        opp_off = request.form.get('opp_off')
        opp_pace = request.form.get('opp_pace')
        win_pct = request.form.get('win_pct')
        home = request.form.get('home')

        if d is None or d == '':
            d = '2023-10-20'
        if opp_def is None or opp_def == '':
            opp_def = '>0'
        if opp_off is None or opp_off == '':
            opp_off = '>0'
        if opp_pace is None or opp_pace == '':
            opp_pace = '>0'
        if win_pct is None or win_pct == '':
            win_pct = '>0'

        if home is None or home == 'all' or home == '':
            home = '!=10'
        elif home == 'home':
            home = '=1'
        else:
            home = '=0'

        return redirect(url_for('views.psearchr', player1=player1, stat=stat, d=d, opp_def=opp_def, opp_off=opp_off,
                                opp_pace=opp_pace, win_pct=win_pct, home=home, base=base))

    return render_template("psearch.html", user=current_user)


@views.route('/gsearch', methods=['GET', 'POST'])
@login_required
def gsearch():
    if request.method == "POST":
        pra = request.form.get('pra')
        min = request.form.get('min')
        pts = request.form.get('pts')
        reb = request.form.get('reb')
        ast = request.form.get('ast')
        home = request.form.get('home')
        gp = request.form.get('gp')
        d = request.form.get('d')

        if min is None or min == '':
            min = 0
        if pra is None or pra == '':
            pra = 0
        if pts is None or pts == '':
            pts = 0
        if reb is None or reb == '':
            reb = 0
        if ast is None or ast == '':
            ast = 0
        if ast is None or ast == '':
            ast = 0
        if gp is None or gp == '':
            gp = 0

        if home is None or home == 'all' or home == '':
            home = '!=10'
        elif home == 'home':
            home = '=1'
        else:
            home = '=0'

        if d is None or d == '':
            d = '2023-12-22'

        return redirect(url_for('views.gsearchr', pra=pra, ast=ast, d=d, reb=reb, pts=pts, home=home, min=min, gp=gp))

    return render_template("gsearch.html", user=current_user)


@views.route('/gsearchr', methods=['GET'])
@login_required
def gsearchr():
    conn = db.engine

    min = request.args.get('min')
    pra = request.args.get('pra')
    pts = request.args.get('pts')
    ast = request.args.get('ast')
    reb = request.args.get('reb')
    home = request.args.get('home')
    g = request.args.get('gp')
    d = request.args.get('d')

    q = f"""select *
            from (SELECT pl.player_name, (select pl1.team from PlayerLog pl1 where pl1.player_name = pl.player_name order by pl1.game_id desc limit 1) as team, round(avg(pl.sp/60),2) `mpg`, round(stddev(pl.sp/60),2) `mpg stddev.`, round(avg(pl.pts+pl.ast+pl.orb+pl.drb),2) `pra`, round(stddev(pl.pts+pl.ast+pl.orb+pl.drb),2) `pra stddev.`, round(100*stddev(pl.pts+pl.ast+pl.orb+pl.drb)/avg(pl.pts+pl.ast+pl.orb+pl.drb),2) `%var pra`, round(avg(pl.pts),2) ppg, round(stddev(pl.pts),2) `ppg stddev.`, round(avg(pl.orb+pl.drb),2) `rpg`, round(stddev(pl.orb+pl.drb),2) `rpg stddev.`, round(avg(pl.ast),2) `apg`, round(stddev(pl.ast),2) `apg stddev.`, round(avg(pl.tp),2) `3pm`, round(stddev(pl.tp),2) `3pm stddev.`, round(avg(pl.blk),2) `blk`, round(stddev(pl.blk),2) `blk stddev.`, round(avg(pl.stl),2) `stl`, round(stddev(pl.stl),2) `stl stddev.`, round(avg(pl.tov),2) `tov`, round(stddev(pl.tov),2) `tov stddev.`,count(*) games
            from PlayerLog pl
            join Game g on g.game_id = pl.game_id
            join team_advanced_stats tas on tas.team = pl.opp
            where g.season = 2024 and pl.sp >0 and g.game_date > greatest('{d}',(CURDATE() - INTERVAL 1 MONTH)) and home{home}
            group by pl.player_name, 2) as t
        where t.`pra`>{pra} and t.`ppg`>{pts} and t.`apg`>{ast} and t.`rpg`>{reb} and t.`mpg`>{min} and t.games >{g}
        order by t.`pra` desc
        limit 100"""

    q = text(q)

    df = pd.read_sql(q, conn, index_col=None)

    return render_template("gsearchr.html", tables=[df.to_html(classes='sortable', index=False)],
                           titles=df.columns.values, user=current_user)


@views.route('/psearchr', methods=['GET'])
@login_required
def psearchr():
    player1 = request.args.get('player1')
    d = request.args.get('d')
    base = request.args.get('base')
    stat = request.args.get('stat')
    opp_def = request.args.get('opp_def')
    opp_off = request.args.get('opp_off')
    opp_pace = request.args.get('opp_pace')
    win_pct = request.args.get('win_pct')
    home = request.args.get('home')

    conn = db.engine

    q = f"""SELECT g.game_date, pl.*, pl.pts + pl.ast + pl.orb + pl.drb pra, pl.orb + pl.drb reb, tas.PACE_RANK opp_pace, tas.REB_PCT_RANK opp_reb_rank, tas.TM_TOV_PCT_RANK opp_tov, tas.OFF_RATING_RANK opp_off, tas.DEF_RATING_RANK opp_def, tas.NET_RATING_RANK opp_net, tas.W_PCT w_pct, (CASE when g.away = pl.opp then 1 else 0 END) home
            from PlayerLog pl
            join Game g on g.game_id = pl.game_id and g.season = 2024
            join team_advanced_stats tas on tas.team = pl.opp and g.game_date = tas.game_date
            where pl.player_name = '{player1}' and g.game_date > '{d}' and tas.PACE_RANK {opp_pace} and tas.DEF_RATING_RANK {opp_def} and tas.OFF_RATING_RANK {opp_off} and tas.W_PCT {win_pct} and (CASE when g.away = pl.opp then 1 else 0 END) {home}
            order by 1"""

    q = text(q)
    df = pd.read_sql(q, conn, index_col=None)

    df = df[
        ['game_date', 'player_name', 'opp', 'home', 'pra', 'pts', 'reb', 'ast', 'stl', 'blk', 'tov', 'tp', 'tpa', 'fg',
         'fga', 'opp_pace', 'opp_def', 'opp_off', 'w_pct']]

    df['home'] = df['home'].apply(lambda x: 'home' if x == 1 else 'away')

    df.rename(
        columns={'game_date': 'Date', 'player_name': 'Player Name', 'opp': 'Opp.', 'home': 'Home/Away', 'tp': '3pm',
                 'fg': 'fgm', 'opp_pace': 'Opp. Pace Rnk', 'opp_def': 'Opp. Def Rnk', 'opp_off': 'Opp. Off Rnk',
                 'w_pct': 'Opp. Win%'}, inplace=True)

    stat_vals = df[stat]
    dates = df['Date']

    fig = Figure()
    ax = fig.subplots()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
    ax.plot(dates, stat_vals, label=f'{player1} {stat}')
    if base != '':
        base = float(base)
        ax.plot(dates, [base] * len(dates), label=f'Base {stat}')
    ax.legend(bbox_to_anchor=(1.04, 1), borderaxespad=0)
    buf = BytesIO()
    fig.savefig(buf, format='png', dpi=175, bbox_inches='tight')
    data = base64.b64encode(buf.getbuffer()).decode("ascii")

    desc = f"This shows a total of {len(dates)} games."
    if base != '':
        pct = round(100 * sum(i > base for i in stat_vals) / len(stat_vals))
        if pct >= 50:
            desc += f"\n{player1} is above the base {base} {stat} in <b><span style='color: green'>{round(100 * sum(i > base for i in stat_vals) / len(stat_vals))}%</span></b> of {len(dates)} games."
        else:
            desc += f"\n{player1} is above the base {base} {stat} in <b><span style='color: red'>{round(100 * sum(i > base for i in stat_vals) / len(stat_vals))}%</span></b> of {len(dates)} games."

    return render_template("psearchr.html", tables=[df.to_html(classes='sortable', index=False)],
                           titles=df.columns.values, img=f"<img src='data:image/png;base64,{data}'", desc=desc,
                           user=current_user)


@views.route('/tstats', methods=['GET'])
@login_required
def tstats():
    conn = db.engine

    q = """SELECT tas.team, tas.DEF_RATING as `Def Rtg`, tas.DEF_RATING_RANK `Def Rtg Rank`, tas.OFF_RATING `Off Rtg`, tas.OFF_RATING_RANK `Off Rtg Rank`, tas.PACE `Pace`, tas.PACE_RANK `Pace Rank`, tas.NET_RATING `Net Rtg`, tas.NET_RATING_RANK `Net Rtg Rank`, tas.REB_PCT_RANK `Reb% Rank`, tas.AST_TO_RANK `Ast/To Rank`, tas.TS_PCT `True Shooting %`, tas.TS_PCT_RANK `True Shooting % Rank`
            from team_advanced_stats tas"""
    q = text(q)
    df = pd.read_sql(q, conn, index_col=None)

    return render_template("tstats.html", tables=[df.to_html(classes='sortable', index=False)],
                           titles=df.columns.values,
                           user=current_user)


@views.route('/playersearch', methods=['GET'])
@login_required
def playersearch():
    pname = request.args.get('pname')

    conn = db.engine.connect()

    q = f"""SELECT p.player_name FROM players p WHERE p.player_name like '%{pname}%' order by p.pts desc"""
    q = text(q)

    data = []
    for row in conn.execute(q):
        data.append({'value': row[0]})

    return jsonify(data)
