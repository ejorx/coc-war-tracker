import os
from datetime import datetime, timezone

from jinja2 import Environment, FileSystemLoader

from service.ApiService import ApiClient
from db.database import Database


def process_war(db: Database):
    """Consulta la guerra actual y guarda participaciones."""
    client = ApiClient()
    war = client.get_current_war()

    if not war:
        print("No se pudo obtener información de guerra.")
        return False

    state = war.get("state")
    print(f"Estado de la guerra: {state}")

    if state not in ("inWar", "warEnded"):
        print("La guerra está en preparación. No hay ataques todavía.")
        return False

    war_end_time = war.get("endTime")

    members = war.get("clan", {}).get("members", [])
    for member in members:
        attacks = member.get("attacks", [])
        stars = sum(a.get("stars", 0) for a in attacks)
        db.upsert_participation(
            player_tag=member.get("tag"),
            player_name=member.get("name"),
            stars=stars,
            attacks=len(attacks),
            war_end_time=war_end_time
        )

    print(f"Actualizados {len(members)} jugadores de la guerra ({state}, {war_end_time}).")
    return True


def generate_html(db: Database):
    """Genera el HTML estático con las estadísticas."""
    players = db.get_player_stats()
    recent_wars = db.get_recent_wars()

    template_dir = os.path.join(os.path.dirname(__file__), "templates")
    output_dir = os.path.join(os.path.dirname(__file__), "docs")
    os.makedirs(output_dir, exist_ok=True)

    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("index.html")

    html = template.render(
        players=players,
        recent_wars=recent_wars,
        updated_at=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    )

    output_path = os.path.join(output_dir, "index.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"HTML generado en {output_path}")


def main():
    db = Database()

    try:
        process_war(db)
        db.purge_old_records(max_age_days=90, max_rows=1000)
        generate_html(db)
    finally:
        db.close()


if __name__ == "__main__":
    main()
