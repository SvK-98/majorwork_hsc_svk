from sukesh_education.app import create_app, db
from flask_migrate import Migrate, upgrade
from alembic.operations import ops

migrate = Migrate(create_app(), db)

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        # Use Flask-Migrate to handle schema updates
        migrate = Migrate(app, db)
        # Create a migration context
        from alembic.migration import MigrationContext
        from alembic.operations import Operations
        conn = db.engine.connect()
        ctx = MigrationContext.configure(conn)
        op = Operations(ctx)
        
        # Check if columns exist before trying to add/remove them
        inspector = db.inspect(db.engine)
        existing_columns = [col['name'] for col in inspector.get_columns('users')]
        
        # Remove year_level column if it exists
        if 'year_level' in existing_columns:
            try:
                op.drop_column('users', 'year_level')
                print("Removed year_level column")
            except Exception as e:
                print(f"Error removing year_level column: {e}")
        
        # Add new columns if they don't exist
        if 'date_of_birth' not in existing_columns:
            try:
                op.add_column('users', db.Column('date_of_birth', db.Date, nullable=True))
                print("Added date_of_birth column")
            except Exception as e:
                print(f"Error adding date_of_birth column: {e}")
        
        if 'address' not in existing_columns:
            try:
                op.add_column('users', db.Column('address', db.String(200), nullable=True))
                print("Added address column")
            except Exception as e:
                print(f"Error adding address column: {e}")
        
        if 'phone_number' not in existing_columns:
            try:
                op.add_column('users', db.Column('phone_number', db.String(20), nullable=True))
                print("Added phone_number column")
            except Exception as e:
                print(f"Error adding phone_number column: {e}")
        
        if 'bio' not in existing_columns:
            try:
                op.add_column('users', db.Column('bio', db.Text, nullable=True))
                print("Added bio column")
            except Exception as e:
                print(f"Error adding bio column: {e}")
        
        print("Database schema updated successfully.")
