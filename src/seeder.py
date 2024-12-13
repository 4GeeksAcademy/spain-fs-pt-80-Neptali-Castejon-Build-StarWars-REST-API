from app import db, app  # Importa db y app desde el archivo principal
from models import Users, Articles, Tags, ArticlesTags  # Asegúrate de que 'models' sea el archivo donde están definidas las clases
from admin import setup_admin  # Asegúrate de importar la configuración de admin

# Configuración de Admin
setup_admin(app)

# Seeder para agregar datos de prueba
def seed_data():
    # Limpiar las tablas para evitar duplicados
    db.session.query(ArticlesTags).delete()
    db.session.query(Articles).delete()
    db.session.query(Users).delete()
    db.session.query(Tags).delete()

    # Crear usuarios
    user1 = Users(email="alice@example.com", password="password123", is_active=True)
    user2 = Users(email="bob@example.com", password="password123", is_active=True)
    
    db.session.add(user1)
    db.session.add(user2)

    # Crear tags
    tag1 = Tags(name="Technology")
    tag2 = Tags(name="Science")
    tag3 = Tags(name="Lifestyle")
    
    db.session.add(tag1)
    db.session.add(tag2)
    db.session.add(tag3)

    # Confirmar las transacciones para usuarios y tags
    db.session.commit()

    # Crear artículos (después de confirmar los usuarios y tags para obtener sus IDs)
    article1 = Articles(title="The Future of AI", content="This article discusses the advancements in AI.", user_id=user1.id)
    article2 = Articles(title="Healthy Living Tips", content="This article gives tips for a healthy lifestyle.", user_id=user2.id)
    
    db.session.add(article1)
    db.session.add(article2)

    # Confirmar las transacciones para artículos
    db.session.commit()

    # Crear relaciones entre artículos y tags
    articlestag1 = ArticlesTags(article_id=article1.id, tag_id=tag1.id, extra_info="AI and its future in technology.")
    articlestag2 = ArticlesTags(article_id=article1.id, tag_id=tag2.id, extra_info="Exploring AI's impact on science.")
    articlestag3 = ArticlesTags(article_id=article2.id, tag_id=tag3.id, extra_info="Health is essential for a good lifestyle.")

    db.session.add(articlestag1)
    db.session.add(articlestag2)
    db.session.add(articlestag3)

    # Confirmar las transacciones para las relaciones
    db.session.commit()

    print("Datos de prueba insertados correctamente.")

# Llamar a la función de seeding
if __name__ == "__main__":
    seed_data()
