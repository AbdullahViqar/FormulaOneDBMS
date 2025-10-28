import mysql.connector as sql
import csv

# -------------------- DATABASE CONNECTION --------------------
con = sql.connect(
    user='root',
    password='palisade',
    unix_socket='/tmp/mysql.sock',
    database='f1test'
)

cursor = con.cursor()
print('✅ Connected to Formula One database successfully!')

# ✅ Create table with constraints
cursor.execute("""
    CREATE TABLE IF NOT EXISTS drivers (
        name VARCHAR(50) PRIMARY KEY,
        team VARCHAR(50) NOT NULL,
        points INT CHECK (points >= 0 AND points <= 500)
    )
""")
con.commit()

# -------------------- FUNCTIONS --------------------

def add_driver():
    name = input("Enter Full Name: ")
    team = input("Enter Team Name: ")
    points = int(input("Enter Points: "))

    # ✅ Validation for points range
    if points < 0 or points > 500:
        print("❌ Points must be between 0 and 500.")
        return

    # ✅ Check for duplicate driver
    cursor.execute("SELECT name FROM drivers WHERE name=%s", (name,))
    if cursor.fetchone():
        print("❌ Driver already exists!")
        return

    cursor.execute("INSERT INTO drivers (name, team, points) VALUES (%s, %s, %s)", (name, team, points))
    con.commit()
    print("✅ Driver added successfully!")


def update_points():
    name = input("Enter Driver Name: ")
    pts = int(input("Enter new points: "))

    # ✅ Validation for points range
    if pts < 0 or pts > 500:
        print("❌ Points must be between 0 and 500.")
        return

    cursor.execute("UPDATE drivers SET points=%s WHERE name=%s", (pts, name))
    if cursor.rowcount == 0:
        print("❌ Driver not found.")
    else:
        con.commit()
        print("✅ Points updated successfully!")


def delete_driver():
    name = input("Enter Driver Name to Delete: ")
    cursor.execute("DELETE FROM drivers WHERE name=%s", (name,))
    if cursor.rowcount == 0:
        print("❌ Driver not found.")
    else:
        con.commit()
        print("✅ Driver deleted successfully!")


def display_all():
    cursor.execute("SELECT * FROM drivers")
    data = cursor.fetchall()
    if not data:
        print("⚠️ No records found.")
        return
    print("\n=== DRIVER LIST ===")
    print(f"{'Name':<20} {'Team':<20} {'Points':<10}")
    print("-" * 50)
    for row in data:
        print(f"{row[0]:<20} {row[1]:<20} {row[2]:<10}")

def leaderboard():

        cursor.execute("SELECT name, team, points FROM drivers ORDER BY points DESC")
        data = cursor.fetchall()
        if not data:
            print("⚠️ No records found.")
            return

        print("\n=== F1 DRIVER LEADERBOARD ===")
        print(f"{'Position':<10} {'Name':<20} {'Team':<25} {'Points':<10}")
        print("-" * 70)
        for idx, row in enumerate(data, start=1):
            print(f"{idx:<10} {row[0]:<20} {row[1]:<25} {row[2]:<10}")

def search_driver():
    name = input("Enter Driver Name to Search: ")
    cursor.execute("SELECT * FROM drivers WHERE name=%s", (name,))
    row = cursor.fetchone()
    if not row:
        print("❌ Driver not found.")
    else:
        print("\n=== DRIVER DETAILS ===")
        print(f"Name: {row[0]}")
        print(f"Team: {row[1]}")
        print(f"Points: {row[2]}")


def export_to_csv():
    cursor.execute("SELECT * FROM drivers")
    rows = cursor.fetchall()
    if not rows:
        print("⚠️ No data to export.")
        return
    with open("drivers.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Team", "Points"])
        writer.writerows(rows)
    print("✅ Data exported to drivers.csv successfully!")


# -------------------- MAIN MENU --------------------
def main():
    while True:
        print("\n=== F1 RACE MANAGEMENT SYSTEM ===")
        print("1. Add Driver")
        print("2. Update Points")
        print("3. Delete Driver")
        print("4. Display All Drivers")
        print("5. Show Leaderboard")
        print("6. Search Driver")
        print("7. Export to CSV")
        print("8. Exit")

        ch = input("Enter your choice: ")

        if ch == '1':
            add_driver()
        elif ch == '2':
            update_points()
        elif ch == '3':
            delete_driver()
        elif ch == '4':
            display_all()
        elif ch == '5':
            leaderboard()
        elif ch == '6':
            search_driver()
        elif ch == '7':
            export_to_csv()
        elif ch == '8':
            print("🏁 Exiting F1 Management System. Goodbye!")
            break
        else:
            print("❌ Invalid choice! Please try again.")


if __name__ == "__main__":
    main()