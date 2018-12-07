# Item Catalog
submitted by [Arushi Doshi](https://github.com/arushidoshi), for completing the fifth project of:
[Full-Stack Web Developer Nanodegree](https://www.udacity.com/course/nd004)

## About This project

The web application provides information on books organised within bookshelves. Users can create, update or delete bookshelves and books. The webapp is powered using Flask, SQLAlchemy and Google and Facebook OAuth.

## Files 

**database_setup.py** -- _Contains the code for setting up the database schema_ 

**lotsofbooks.py** -- _Contains the code to populate the database with a few bookshelves and books_  

**my_project.py** -- _Contains the code to setup the webapp and provide functionality_  

## Prerequisites 

1. Download [Virtual Box](https://www.virtualbox.org/wiki/Downloads) to run the virtual machine
2. Download the latest build of [Vagrant](https://www.vagrantup.com/downloads.html)
3. Clone [this](https://github.com/arushidoshi/item-catalog) repository and download it on your computer

## Instructions

1. To start Vagrant
   - Open Terminal or cmd and browse to the vagrant folder
   - Type `vagrant up`
2. SSH into the vagrant VM
   - In the same terminal type `vagrant ssh`
3. Change to the correct folder
   - Type `cd /vagrant/catalog`
4. To prepare the database
   - Type `python database_setup.py`
   - Type `python lotsofbooks.py`
5. To run the webapp
   - Type `python my_project.py`

## Expected Outcomes
- Without logging in:
  - Users can view all books and bookshelves
- Logging in using Google or Facebook:
   - Users can add bookshelves
   - Users can update or delete bookshelves created by them
   - Users can add books to the bookshelves created by them
   - Users can update of delete books created by them 

## License
The content of this repository is licensed under [MIT License](https://opensource.org/licenses/MIT)
