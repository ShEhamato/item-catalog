
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Catalog, Base, CatalogItem

engine = create_engine('sqlite:///catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Menu for UrbanBurger
catalog1 = Catalog(name="Accounting / Finance", description='Financial accounting is a specialized branch of accounting that keeps track of a company financial transactions')


session.add(catalog1)
session.commit()

catalogItem2 = CatalogItem(name="Audit and taxation", description="Auditing & Taxation can be studied as a single subject or as part of one of our Professional Qualifications.",
                     price="$200", duration="3 months", catalog=catalog1)

session.add(catalogItem2)
session.commit()


catalogItem1 = CatalogItem(name="Banking/ Finance", description="Banking and Finance (Hons) programme is designed to provide the students with knowledge and skills in handling financial products",
                     price="$300", duration="2 months", catalog=catalog1)

session.add(catalogItem1)
session.commit()

catalogItem2 = CatalogItem(name="Corporate / Finance Investment", description="Corporate finance is an area of finance that deals with sources of funding, the capital structure of corporations, the actions that managers take to increase the value of the firm to the shareholders, and the tools and analysis used to allocate financial resources.",
                     price="$500", duration="4 months", catalog=catalog1)

session.add(catalogItem2)
session.commit()

catalogItem3 = CatalogItem(name="General/ Cost Accounting", description="Cost accounting is an accounting method that aims to capture a company's costs of production by assessing the input costs of each step of production as well as fixed costs",
                     price="$150", duration="2 months", catalog=catalog1)

session.add(catalogItem3)
session.commit()

# Menu for Super Stir Fry
catalog2 = Catalog(name="Super Stir Fry")

session.add(catalog2)
session.commit()


catalogItem1 = CatalogItem(name="Chicken Stir Fry", description="With your choice of noodles vegetables and sauces",
                     price="$7.99", duration="Entree", catalog=catalog2)

session.add(catalogItem1)
session.commit()

catalogItem2 = CatalogItem(
    name="Peking Duck", description=" A famous duck dish from Beijing[1] that has been prepared since the imperial era. The meat is prized for its thin, crisp skin, with authentic versions of the dish serving mostly the skin and little meat, sliced in front of the diners by the cook", price="$25", duration="Entree", catalog=catalog2)

session.add(catalogItem2)
session.commit()

catalogItem3 = CatalogItem(name="Spicy Tuna Roll", description="Seared rare ahi, avocado, edamame, cucumber with wasabi soy sauce ",
                     price="15", duration="Entree", catalog=catalog2)

session.add(catalogItem3)
session.commit()

catalogItem4 = CatalogItem(name="Nepali Momo ", description="Steamed dumplings made with vegetables, spices and meat. ",
                     price="12", duration="Entree", catalog=catalog2)

session.add(catalogItem4)
session.commit()

catalogItem5 = CatalogItem(name="Beef Noodle Soup", description="A Chinese noodle soup made of stewed or red braised beef, beef broth, vegetables and Chinese noodles.",
                     price="14", duration="Entree", catalog=catalog2)

session.add(catalogItem5)
session.commit()

catalogItem6 = CatalogItem(name="Ramen", description="a Japanese noodle soup dish. It consists of Chinese-style wheat noodles served in a meat- or (occasionally) fish-based broth, often flavored with soy sauce or miso, and uses toppings such as sliced pork, dried seaweed, kamaboko, and green onions.",
                     price="12", duration="Entree", catalog=catalog2)

session.add(catalogItem6)
session.commit()


# Menu for Panda Garden
catalog1 = Catalog(name="Panda Garden")

session.add(catalog1)
session.commit()


catalogItem1 = CatalogItem(name="Pho", description="a Vietnamese noodle soup consisting of broth, linguine-shaped rice noodles called banh pho, a few herbs, and meat.",
                     price="$8.99", duration="Entree", catalog=catalog1)

session.add(catalogItem1)
session.commit()

catalogItem2 = CatalogItem(name="Chinese Dumplings", description="a common Chinese dumpling which generally consists of minced meat and finely chopped vegetables wrapped into a piece of dough skin. The skin can be either thin and elastic or thicker.",
                     price="$6.99", duration="Appetizer", catalog=catalog1)

session.add(catalogItem2)
session.commit()

catalogItem3 = CatalogItem(name="Gyoza", description="The most prominent differences between Japanese-style gyoza and Chinese-style jiaozi are the rich garlic flavor, which is less noticeable in the Chinese version, the light seasoning of Japanese gyoza with salt and soy sauce, and the fact that gyoza wrappers are much thinner",
                     price="$9.95", duration="Entree", catalog=catalog1)

session.add(catalogItem3)
session.commit()

catalogItem4 = CatalogItem(name="Stinky Tofu", description="Taiwanese dish, deep fried fermented tofu served with pickled cabbage.",
                     price="$6.99", duration="Entree", catalog=catalog1)

session.add(catalogItem4)
session.commit()

catalogItem2 = CatalogItem(name="Veggie Burger", description="Juicy grilled veggie patty with tomato mayo and lettuce",
                     price="$9.50", duration="Entree", catalog=catalog1)

session.add(catalogItem2)
session.commit()


# Menu for Thyme for that
catalog1 = Catalog(name="Thyme for That Vegetarian Cuisine ")

session.add(catalog1)
session.commit()


catalogItem1 = CatalogItem(name="Tres Leches Cake", description="Rich, luscious sponge cake soaked in sweet milk and topped with vanilla bean whipped cream and strawberries.",
                     price="$2.99", duration="Dessert", catalog=catalog1)

session.add(catalogItem1)
session.commit()

catalogItem2 = CatalogItem(name="Mushroom risotto", description="Portabello mushrooms in a creamy risotto",
                     price="$5.99", duration="Entree", catalog=catalog1)

session.add(catalogItem2)
session.commit()

catalogItem3 = CatalogItem(name="Honey Boba Shaved Snow", description="Milk snow layered with honey boba, jasmine tea jelly, grass jelly, caramel, cream, and freshly made mochi",
                     price="$4.50", duration="Dessert", catalog=catalog1)

session.add(catalogItem3)
session.commit()

catalogItem4 = CatalogItem(name="Cauliflower Manchurian", description="Golden fried cauliflower florets in a midly spiced soya,garlic sauce cooked with fresh cilantro, celery, chilies,ginger & green onions",
                     price="$6.95", duration="Appetizer", catalog=catalog1)

session.add(catalogItem4)
session.commit()

catalogItem5 = CatalogItem(name="Aloo Gobi Burrito", description="Vegan goodness. Burrito filled with rice, garbanzo beans, curry sauce, potatoes (aloo), fried cauliflower (gobi) and chutney. Nom Nom",
                     price="$7.95", duration="Entree", catalog=catalog1)

session.add(catalogItem5)
session.commit()

catalogItem2 = CatalogItem(name="Veggie Burger", description="Juicy grilled veggie patty with tomato mayo and lettuce",
                     price="$6.80", duration="Entree", catalog=catalog1)

session.add(catalogItem2)
session.commit()


# Menu for Tony's Bistro
catalog1 = Catalog(name="Tony\'s Bistro ")

session.add(catalog1)
session.commit()


catalogItem1 = CatalogItem(name="Shellfish Tower", description="Lobster, shrimp, sea snails, crawfish, stacked into a delicious tower",
                     price="$13.95", duration="Entree", catalog=catalog1)

session.add(catalogItem1)
session.commit()

catalogItem2 = CatalogItem(name="Chicken and Rice", description="Chicken... and rice",
                     price="$4.95", duration="Entree", catalog=catalog1)

session.add(catalogItem2)
session.commit()

catalogItem3 = CatalogItem(name="Mom's Spaghetti", description="Spaghetti with some incredible tomato sauce made by mom",
                     price="$6.95", duration="Entree", catalog=catalog1)

session.add(catalogItem3)
session.commit()

catalogItem4 = CatalogItem(name="Choc Full O\' Mint (Smitten\'s Fresh Mint Chip ice cream)",
                     description="Milk, cream, salt, ..., Liquid nitrogen magic", price="$3.95", duration="Dessert", catalog=catalog1)

session.add(catalogItem4)
session.commit()

catalogItem5 = CatalogItem(name="Tonkatsu Ramen", description="Noodles in a delicious pork-based broth with a soft-boiled egg",
                     price="$7.95", duration="Entree", catalog=catalog1)

session.add(catalogItem5)
session.commit()


# Menu for Andala's
catalog1 = Catalog(name="Andala\'s")

session.add(catalog1)
session.commit()


catalogItem1 = CatalogItem(name="Lamb Curry", description="Slow cook that thang in a pool of tomatoes, onions and alllll those tasty Indian spices. Mmmm.",
                     price="$9.95", duration="Entree", catalog=catalog1)

session.add(catalogItem1)
session.commit()

catalogItem2 = CatalogItem(name="Chicken Marsala", description="Chicken cooked in Marsala wine sauce with mushrooms",
                     price="$7.95", duration="Entree", catalog=catalog1)

session.add(catalogItem2)
session.commit()

catalogItem3 = CatalogItem(name="Potstickers", description="Delicious chicken and veggies encapsulated in fried dough.",
                     price="$6.50", duration="Appetizer", catalog=catalog1)

session.add(catalogItem3)
session.commit()

catalogItem4 = CatalogItem(name="Nigiri Sampler", description="Maguro, Sake, Hamachi, Unagi, Uni, TORO!",
                     price="$6.75", duration="Appetizer", catalog=catalog1)

session.add(catalogItem4)
session.commit()

catalogItem2 = CatalogItem(name="Veggie Burger", description="Juicy grilled veggie patty with tomato mayo and lettuce",
                     price="$7.00", duration="Entree", catalog=catalog1)

session.add(catalogItem2)
session.commit()


# Menu for Auntie Ann's
catalog1 = Catalog(name="Auntie Ann\'s Diner ")

session.add(catalog1)
session.commit()

catalogItem9 = CatalogItem(name="Chicken Fried Steak", description="Fresh battered sirloin steak fried and smothered with cream gravy",
                     price="$8.99", duration="Entree", catalog=catalog1)

session.add(catalogItem9)
session.commit()


catalogItem1 = CatalogItem(name="Boysenberry Sorbet", description="An unsettlingly huge amount of ripe berries turned into frozen (and seedless) awesomeness",
                     price="$2.99", duration="Dessert", catalog=catalog1)

session.add(catalogItem1)
session.commit()

catalogItem2 = CatalogItem(name="Broiled salmon", description="Salmon fillet marinated with fresh herbs and broiled hot & fast",
                     price="$10.95", duration="Entree", catalog=catalog1)

session.add(catalogItem2)
session.commit()

catalogItem3 = CatalogItem(name="Morels on toast (seasonal)", description="Wild morel mushrooms fried in butter, served on herbed toast slices",
                     price="$7.50", duration="Appetizer", catalog=catalog1)

session.add(catalogItem3)
session.commit()

catalogItem4 = CatalogItem(name="Tandoori Chicken", description="Chicken marinated in yoghurt and seasoned with a spicy mix(chilli, tamarind among others) and slow cooked in a cylindrical clay or metal oven which gets its heat from burning charcoal.",
                     price="$8.95", duration="Entree", catalog=catalog1)

session.add(catalogItem4)
session.commit()

catalogItem2 = CatalogItem(name="Veggie Burger", description="Juicy grilled veggie patty with tomato mayo and lettuce",
                     price="$9.50", duration="Entree", catalog=catalog1)

session.add(catalogItem2)
session.commit()

catalogItem10 = CatalogItem(name="Spinach Ice Cream", description="vanilla ice cream made with organic spinach leaves",
                      price="$1.99", duration="Dessert", catalog=catalog1)

session.add(catalogItem10)
session.commit()


# Menu for Cocina Y Amor
catalog1 = Catalog(name="Cocina Y Amor ")

session.add(catalog1)
session.commit()


catalogItem1 = CatalogItem(name="Super Burrito Al Pastor", description="Marinated Pork, Rice, Beans, Avocado, Cilantro, Salsa, Tortilla",
                     price="$5.95", duration="Entree", catalog=catalog1)

session.add(catalogItem1)
session.commit()

catalogItem2 = CatalogItem(name="Cachapa", description="Golden brown, corn-based Venezuelan pancake; usually stuffed with queso telita or queso de mano, and possibly lechon. ",
                     price="$7.99", duration="Entree", catalog=catalog1)

session.add(catalogItem2)
session.commit()


catalog1 = Catalog(name="State Bird Provisions")
session.add(catalog1)
session.commit()

catalogItem1 = CatalogItem(name="Chantrelle Toast", description="Crispy Toast with Sesame Seeds slathered with buttery chantrelle mushrooms",
                     price="$5.95", duration="Appetizer", catalog=catalog1)

session.add(catalogItem1)
session.commit()

catalogItem1 = CatalogItem(name="Guanciale Chawanmushi", description="Japanese egg custard served hot with spicey Italian Pork Jowl (guanciale)",
                     price="$6.95", duration="Dessert", catalog=catalog1)

session.add(catalogItem1)
session.commit()


catalogItem1 = CatalogItem(name="Lemon Curd Ice Cream Sandwich", description="Lemon Curd Ice Cream Sandwich on a chocolate macaron with cardamom meringue and cashews",
                     price="$4.25", duration="Dessert", catalog=catalog1)

session.add(catalogItem1)
session.commit()


print "added menu items!"