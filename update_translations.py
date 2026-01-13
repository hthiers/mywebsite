"""
Script to update existing portfolio articles with English translations.
Run this once to add English content to your existing articles.
"""
from database import update_article, get_all_articles

def update_portfolio_translations():
    """Add English translations to existing portfolio articles."""

    print("Updating portfolio articles with English translations...")

    # Get existing articles
    articles = get_all_articles()

    # English translations mapped by Spanish title
    translations = {
        'Relok - Sistema de Control de Tiempos': {
            'title_en': 'Relok - Time Tracking System',
            'description_en': 'Web application developed for work time management and tracking. Includes automatic reports, project integration, and analytical dashboard.'
        },
        'Pipeline ETL en Snowflake': {
            'title_en': 'ETL Pipeline in Snowflake',
            'description_en': 'Migration and optimization of notebooks to stored procedures in Snowflake. Massive data processing with Python and automated orchestration.'
        },
        'Sistema de Business Intelligence': {
            'title_en': 'Business Intelligence System',
            'description_en': 'Complete BI solution implementation with Metabase and Docker. Interactive dashboards and automated reports for decision making.'
        }
    }

    for article in articles:
        if article['title'] in translations:
            trans = translations[article['title']]
            success = update_article(
                article_id=article['id'],
                title=article['title'],
                description=article['description'],
                tech_stack=article['tech_stack'],
                title_en=trans['title_en'],
                description_en=trans['description_en']
            )
            if success:
                print(f"✓ Updated article: {article['title']}")
            else:
                print(f"✗ Failed to update article: {article['title']}")
        else:
            print(f"⚠ No translation found for: {article['title']}")

    print("\nTranslations updated successfully!")

if __name__ == '__main__':
    update_portfolio_translations()
