"""
Seed script to populate the database with initial portfolio articles.
Run this script once to add sample data to your database.
"""
from database import init_db, create_article

def seed_portfolio():
    """Add initial portfolio articles to the database."""
    # Initialize database if it doesn't exist
    init_db()

    # Portfolio articles from the original prototype
    articles = [
        {
            'title': 'Relok - Sistema de Control de Tiempos',
            'description': 'Aplicación web desarrollada para gestión y seguimiento de tiempos de trabajo. Incluye reportes automáticos, integración con proyectos y dashboard analítico.',
            'title_en': 'Relok - Time Tracking System',
            'description_en': 'Web application developed for work time management and tracking. Includes automatic reports, project integration, and analytical dashboard.',
            'tech_stack': ['Laravel', 'React', 'MySQL', 'Docker'],
            'image_gradient': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            'image_letter': 'R'
        },
        {
            'title': 'Pipeline ETL en Snowflake',
            'description': 'Migración y optimización de notebooks a stored procedures en Snowflake. Procesamiento de datos masivos con Python y orquestación automatizada.',
            'title_en': 'ETL Pipeline in Snowflake',
            'description_en': 'Migration and optimization of notebooks to stored procedures in Snowflake. Massive data processing with Python and automated orchestration.',
            'tech_stack': ['Python', 'Snowflake', 'SQL', 'ETL'],
            'image_gradient': 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
            'image_letter': '🔄'
        },
        {
            'title': 'Sistema de Business Intelligence',
            'description': 'Implementación completa de solución BI con Metabase y Docker. Dashboards interactivos y reportes automatizados para toma de decisiones.',
            'title_en': 'Business Intelligence System',
            'description_en': 'Complete BI solution implementation with Metabase and Docker. Interactive dashboards and automated reports for decision making.',
            'tech_stack': ['Metabase', 'Docker', 'PostgreSQL', 'BI'],
            'image_gradient': 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
            'image_letter': '🏢'
        }
    ]

    print("Seeding database with portfolio articles...")

    for article in articles:
        article_id = create_article(
            title=article['title'],
            description=article['description'],
            tech_stack=article['tech_stack'],
            image_gradient=article['image_gradient'],
            image_letter=article['image_letter'],
            title_en=article.get('title_en'),
            description_en=article.get('description_en'),
            image_url=article.get('image_url')
        )
        print(f"✓ Created article: {article['title']} (ID: {article_id})")

    print("\nDatabase seeded successfully!")
    print("You can now run 'python app.py' to start the application.")

if __name__ == '__main__':
    seed_portfolio()
