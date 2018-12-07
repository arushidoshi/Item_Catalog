from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Bookshelf, Book, User

engine = create_engine('sqlite:///booklibrary.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
"""
A DBSession() instance establishes all conversations with the database
and represents a "staging zone" for all the objects loaded into the
database session object. Any change made against the objects in the
session won't be persisted into the database until you call
session.commit(). If you're not happy about the changes, you can
revert all of them back to the last commit by calling
session.rollback()
"""
session = DBSession()


# Create dummy user
User1 = User(name="Aurora", email="aurora@ymail.com",
             picture='https://i.imgur.com/aQrelO1.png')
session.add(User1)
session.commit()

# Books in 'My 2016 Bookshelf'
bookshelf1 = Bookshelf(user_id=1, name="My 2016 Bookshelf")

session.add(bookshelf1)
session.commit()

book1 = Book(user_id=1, name="The Lightning Thief",
             description="After learning that he is the son of a mortal woman"
             " and Poseidon, god of the sea, twelve-year-old Percy is sent to "
             "a summer camp for demigods like himself, and joins his new "
             "friends on a quest to prevent a war between the gods.",
             author="Rick Riordan", genre="Fantasy",
             status="Read", bookshelf=bookshelf1)

session.add(book1)
session.commit()


book2 = Book(user_id=1, name="The Sea of Monsters", description="Percy and "
             "his friends must journey into the Sea of Monsters to save their"
             " camp. But first, Percy will discover a stunning new secret "
             "about his family--one that makes him question whether being "
             "claimed as Poseidon's son is an honor or simply a cruel joke.",
             author="Rick Riordan", genre="Fantasy", status="Want to Read",
             bookshelf=bookshelf1)

session.add(book2)
session.commit()

book3 = Book(user_id=1, name="Harry Potter and the Philosopher's Stone",
             description="Harry Potter, a boy who learns on his eleventh "
             "birthday that he is the orphaned son of two powerful wizards "
             "and possesses unique magical powers of his own. He is "
             "summoned from his life as an unwanted child to become a student"
             " at Hogwarts, an English boarding school for wizards. There, "
             "he meets several friends who become his closest allies and "
             "help him discover the truth about his parents' deaths.",
             author="J.K. Rowling", genre="Fantasy",
             status="Read", bookshelf=bookshelf1)

session.add(book3)
session.commit()

book4 = Book(user_id=1, name="It's All in the Planets",
             description="Aniket and Nidhi meet on a train, a chance "
             "encounter and she agrees to become his 'relationship coach'. "
             "It's a decision that sets into motion a chain of events that "
             "will have a profound impact on the lives of all involved. "
             "One man, two women and the trap called Destiny. Some things, "
             "they say, are all in the planets.", author="Preeti Shenoy",
             genre="Romance", status="Want to Read", bookshelf=bookshelf1)

session.add(book4)
session.commit()

book5 = Book(user_id=1, name="The Immortals of Meluha",
             description="This once proud empire and its Suryavanshi rulers "
             "face severe perils as its primary river, the revered Saraswati,"
             "is slowly drying to extinction. They also face devastating "
             "terrorist attacks from the east, the land of the "
             "Chandravanshis. The only hope for the Suryavanshis is an "
             "ancient legend: When evil reaches epic proportions, "
             "when all seems lost, when it appears that your enemies have "
             "triumphed, a hero will emerge!", author="Amish Tripathi",
             genre="Mythology", status="Currently Reading",
             bookshelf=bookshelf1)


# Books in 'Must Read Once'
bookshelf2 = Bookshelf(user_id=1, name="Must Read Once")

session.add(bookshelf2)
session.commit()


book1 = Book(user_id=1, name="To Kill a Mockingbird",
             description="The story takes place in a small Alabama town in "
             "the 1930s and is told predominately from the point of view of "
             "a young girl Jean Louise (Scout) Finch. She is the daughter "
             "of Atticus Finch, a white lawyer hired to defend Tom Robinson, "
             "a black man falsely accused of raping a white woman.",
             author="Harper Lee", genre="Historical Fiction",
             status="Not Read", bookshelf=bookshelf2)

session.add(book1)
session.commit()

book2 = Book(user_id=1, name="1984", description="The book offers political"
             " satirist George Orwell's nightmare vision of a totalitarian, "
             "bureaucratic world and one poor stiff's attempt to find "
             "individuality. The brilliance of the novel is Orwell's "
             "prescience of modern life - the ubiquity of television, the "
             "distortion of the language and his ability to construct a "
             "thorough version of hell.", author="George Orwell",
             genre="Dystopia", status="Not Read", bookshelf=bookshelf2)

session.add(book2)
session.commit()

book3 = Book(user_id=1, name="The Book Thief", description="It is 1939. "
             "Nazi Germany. The country is holding its breath. Death has "
             "never been busier, and will become busier still. Liesel "
             "Meminger is a foster girl living outside of Munich, who "
             "scratches out a meager existence for herself by stealing "
             "when she encounters something she can't resist-books. "
             "With the help of her accordion-playing foster father, "
             "she learns to read and shares her stolen books with her "
             "neighbors during bombing raids as well as with the Jewish man"
             " hidden in her basement.", author="Markus Zusak",
             genre="Fiction", status="Currently Reading",
             bookshelf=bookshelf2)

session.add(book3)
session.commit()

book4 = Book(user_id=1, name="Harry Potter and the Deathly Hallows",
             description="The protective charm that has kept Harry "
             "safe until now is broken. But the Dark Lord is breathing "
             "fear into everything he loves. And he knows he can't keep "
             "hiding. To stop Voldemort, Harry knows he must find the "
             "remaining Horcruxes and destroy them. He will have to face "
             "his enemy in one final battle.",
             author="J.K. Rowling", genre="Fantasy", status="Read",
             bookshelf=bookshelf2)

session.add(book4)
session.commit()

book5 = Book(user_id=1, name="Little Women", description="Generations of "
             "readers young and old, male and female, have fallen in love "
             "with the March sisters of Louisa May Alcott's most popular "
             "and enduring novel, Little Women. Here are talented tomboy "
             "and author-to-be Jo, tragically frail Beth, beautiful Meg, "
             "and romantic, spoiled Amy, united in their devotion to each "
             "other and their struggles to survive in New England during "
             "the Civil War.", author="Louisa May Alcott", genre="Classics",
             status="Want to Read", bookshelf=bookshelf2)

session.add(book5)
session.commit()

book6 = Book(user_id=1, name="The Hobbit", description="Bilbo Baggins is a "
             "hobbit who enjoys a comfortable, unambitious life, rarely "
             "traveling any farther than his pantry or cellar. But his "
             "contentment is disturbed when the wizard Gandalf and a "
             "company of dwarves arrive on his doorstep one day to whisk "
             "him away on an adventure. They have launched a plot to raid "
             "the treasure hoard guarded by Smaug the Magnificent, a "
             "large and very dangerous dragon.", author="J.R.R. Tolkien",
             genre="Fantasy", status="Read", bookshelf=bookshelf2)

session.add(book6)
session.commit()


# Books in 'Best of Fiction'
bookshelf3 = Bookshelf(user_id=1, name="Best of Fiction")

session.add(bookshelf3)
session.commit()


book1 = Book(user_id=1, name="The Kite Runner",
             description="A sweeping story of family, love, and friendship "
             "told against the devastating backdrop of the history of "
             "Afghanistan over the last thirty years, The Kite Runner is an "
             "unusual and powerful novel that has become a beloved, "
             "one-of-a-kind classic.", author="Khaled Hosseini",
             genre="Historical Fiction", status="Want to Read",
             bookshelf=bookshelf3)

session.add(book1)
session.commit()

book2 = Book(user_id=1, name="The Chronicles of Narnia",
             description="NARNIA...the land beyond the wardrobe, the secret "
             "country known only to Peter, Susan, Edmund, and Lucy - the "
             "place where the adventure begins. In the blink of an eye, "
             "their lives are changed forever", author="C.S. Lewis",
             genre="YA Fiction", status="Read", bookshelf=bookshelf3)

session.add(book2)
session.commit()

book3 = Book(user_id=1, name="The Devil wears Parda",
             description="This book is about a young woman who is hired as a "
             "personal assistant to a powerful fashion magazine editor, a job"
             " that becomes nightmarish as she struggles to keep up with her "
             "boss's grueling schedule and demeaning demands.",
             author="Lauren Weisberger", genre="Contemporary Fiction",
             status="Not Read", bookshelf=bookshelf3)

session.add(book3)
session.commit()

book4 = Book(user_id=1, name="Artemis Fowl", description="Twelve-year-old "
             "Artemis Fowl is a millionaire, a genius-and, above all, a "
             "criminal mastermind. But even Artemis doesn't know what "
             "he's taken on when he kidnaps a fairy, Captain Holly Short "
             "of the LEPrecon Unit. These aren't the fairies of bedtime "
             "stories-they're dangerous! Full of unexpected twists and "
             "turns, Artemis Fowl is a riveting, magical adventure.",
             author="Eoin Colfer", genre="YA Fiction",
             status="Read", bookshelf=bookshelf3)

session.add(book4)
session.commit()


# Books in 'Award winning books'
bookshelf4 = Bookshelf(user_id=1, name="Award winning books")

session.add(bookshelf4)
session.commit()


book1 = Book(user_id=1, name="Digital Fortress",
             description="From the underground hallways of power to the "
             "skyscrapers of Tokyo to the towering cathedrals of Spain, a "
             "desperate race unfolds. It is a battle for survival - a crucial"
             " bid to destroy a creation of inconceivable genius... an "
             "impregnable code-writing formula that threatens to obliterate "
             "the post-cold war balance of power. Forever.",
             author="Dan Brown", genre="Thriller",
             status="Read", bookshelf=bookshelf4)

session.add(book1)
session.commit()

book2 = Book(user_id=1, name="Paper Towns", description="Quentin Jacobsen "
             "has spent a lifetime loving the magnificently adventurous "
             "Margo Roth Spiegelman from afar. So when she cracks open a "
             "window and climbs into his life, dressed like a ninja and "
             "summoning him for an ingenious campaign of revenge-he follows. "
             "After their all-nighter ends and a new day breaks, Q arrives "
             "at school to discover that Margo, has now become a mystery. "
             "But Q soon learns that there are clues-and they're for him. "
             "Urged down a disconnected path, the closer he gets, the less "
             "Q sees the girl he thought he knew...",
             author="John Green", genre="Contemporary", status="Want to Read",
             bookshelf=bookshelf4)

session.add(book2)
session.commit()

book3 = Book(user_id=1, name="The Selection", description="For thirty-five "
             "girls, the Selection is the chance of a lifetime. The "
             "opportunity to escape the life laid out for them since birth. "
             "To be swept up in a world of glittering gowns and priceless "
             "jewels. But for America Singer, being Selected is a nightmare."
             "It means turning her back on her secret love with Aspen, who "
             "is a caste below her. Then America meets Prince Maxon. "
             "Gradually, she starts to question all the plans she's"
             " made for herself, and realizes that the life she's always "
             "dreamed of may not compare to a future she never imagined.",
             author="Kiera Cass", genre="Romance", status="Currently Reading",
             bookshelf=bookshelf4)

session.add(book3)
session.commit()

book4 = Book(user_id=1, name="Divergent", description="The book features a "
             "post-apocalyptic version of Chicago and follows Beatrice Prior "
             "as she explores her identity within a society that defines its "
             "citizens by their social and personality-related affiliation "
             "with five factions, which removes the threat of anyone "
             "exercising independent will and threatening the population's "
             "safety.", author="Veronica Roth", genre="Dystopia",
             status="Not Read", bookshelf=bookshelf4)

session.add(book4)
session.commit()

book5 = Book(user_id=1, name="Charlie and the Chocolate Factory",
             description="Willy Wonka's famous chocolate factory is opening "
             "at last! But only five lucky children will be allowed inside. "
             "And the winners are: Augustus Gloop, an enormously fat boy "
             "whose hobby is eating; Veruca Salt, a spoiled-rotten brat "
             "whose parents are wrapped around her little finger; Violet "
             "Beauregarde, a gum-chewer with the fastest jaws around;"
             " Mike Teavee, who is obsessed with television; and Charlie"
             " Bucket, a boy who is honest and kind, brave and true,"
             " and good and ready for the wildest time of his life! ",
             author="Roald Dahl", genre="Fantasy", status="Want to Read",
             bookshelf=bookshelf4)

session.add(book5)
session.commit()


# Books in 'Favourites across Genres'
bookshelf5 = Bookshelf(user_id=1, name="Favourites across Genres")

session.add(bookshelf5)
session.commit()


book1 = Book(user_id=1, name="The Girl on the Train",
             description="Rachel catches the same commuter train every "
             "She knows it will wait at the same signal each time, "
             "overlooking a morning. row of back gardens. She's even started "
             "to feel like she knows the people who live in one of the "
             "houses. Jess and Jason, she calls them. Their life looks "
             "perfect. And then she sees something shocking. It's only a "
             "minute until the train moves on, but it's enough. Now "
             "everything's changed. Now Rachel has a chance to become a "
             "part of the lives she's only watched from afar. Now "
             "they'll see; she's much more than just the girl on the train.",
             author="Paula Hawkins", genre="Thriller", status="Read",
             bookshelf=bookshelf5)

session.add(book1)
session.commit()

book2 = Book(user_id=1, name="The Murder of Roger Ackroyd",
             description="Recently retired Hercule Poirot investigates a "
             "neighbor's murder and the disappearance of the deceased's "
             "adopted son.", author="Agatha Christie", genre="Mystery",
             status="Not Read", bookshelf=bookshelf5)

session.add(book2)
session.commit()

book3 = Book(user_id=1, name="Murder on the Orient Express",
             description="What more can a mystery addict desire than a "
             "much-loathed murder victim found aboard the luxurious Orient "
             "Express with multiple stab wounds, thirteen likely suspects, "
             "an incomparably brilliant detective in Hercule Poirot, and the "
             "most ingenious crime ever conceived?", author="Agatha Christie",
             genre="Crime", status="Not Read", bookshelf=bookshelf5)

session.add(book3)
session.commit()

book4 = Book(user_id=1, name="The Cuckoo's Egg", description="Before the "
             "Internet became widely known as a global tool for terrorists, "
             "perceptive U.S. citizen recognized its ominous potential. "
             "Armed one with clear evidence of computer espionage, he began "
             "a highly personal quest to expose a hidden network of spies "
             "that threatened national security.", author="Clifford Stoll",
             genre="Science", status="Want to Read", bookshelf=bookshelf5)

session.add(book4)
session.commit()


book5 = Book(user_id=1, name="Crazy Rich Asians",
             description="Crazy Rich Asians is the outrageously funny debut "
             "novel about three super-rich, pedigreed Chinese families and "
             "the gossip, backbiting, and scheming that occurs when the heir "
             "to one of the most massive fortunes in Asia brings home his "
             "ABC girlfriend to the wedding of the season.",
             author="Kevin Kwan", genre="Romance", status="Read",
             bookshelf=bookshelf5)

session.add(book5)
session.commit()


print "Your library is ready and organised!"
