Groepswerk

Idee:
  - App maken om gemakkelijk de stock te beheren voor mijn band. Voorlopig enkel webversie, Iphone zal later pas kunnen.
  - Concurrentie is BigCartel en Shopify
  - Voorbeeld van onze huidige webshop : https://rejectthesickness.bigcartel.com/
Geeky stuf:
  - Artikelnummer generator:
    - In python wil ik een artikelgenerator die
      De eerste 4 cijfers neemt uit tabel 'releaseyear' 
      De volgende 2 cijfers uit 'Limited Edition'
      De volgende 2 cijfers uit 'Designs'
      De volgende 2 cijfers uit 'producttype'
      De volgende 2 cijfers uit 'Sizes'
    Belangrijk : als het getal in de tabel maar uit 1 cijfer bestaat, moet er een 0 voor   komen (bvb 1 wordt 01)
        De tabellen zitten allemaal in de database 'Reject The Sickness App' (postgreSQL, wordt nog geupload)

Tabellen in Database: 

1.	Articles:
UITLEG : deze tabel houdt de stock van een artikel bij (misschien als View zetten)
-	Articlenr : Wordt gegenereerd door de artikelnummer generator (zie beschrijving hierboven)
-	Producttype: Wordt gelinkt aan de tabel met dezelfde naam
-	Design: Wordt gelinkt aan de Design tabel
-	Companyname : wordt gelinkt aan Company tabel
-	Size : wordt gelinkt aan de Sizes tabel
-	Quantity : toont hoeveel stock van dit artikel nog beschikbaar is

2.	Company:
UITLEG : Deze tabel houdt de leveranciers bij (waar dus de producten gekocht worden
-	Companynr: Primary Key :
-	Companyname: link met Articles
-	Address : Spreekt voor zich
-	Postalcode : hoort bij adres
-	Location:
-	Country:

3.	Designs:
UITLEG: Deze tabel houdt de namen van de Designs bij. Designs kunnen voor meerdere types artikelen gebruikt worden (bvb CD en T-shirt van dezelfde print)
-	Designnr: Primary Key, wordt ingegeven via nieuw Design
-	Designname: wordt ingegeven via nieuw Design en gelinkt aan Articles

4.	Limited_edition:
UITLEG:Kleine tabel die een extra nummer geeft voor de artikelen (wel of niet Limited Edition)
-	Lenr: Primary Key
-	LE: Slecht 2 waarden : Limited Edition of Regular 
-	Opmerking : deze tabel best niet laten veranderen

5.	Producttype:
UITLEG : Deze tabel houdt bij welk type een product is ; bvb CD, Vinyl, Tshirt…
-	 Typenr: Primary Key : deze wordt ingegeven via nieuw type (krijgt automatisch een opvolgend nummer
-	Typename : bvb CD…

6.	Releaseyear:
UITLEG : In deze tabel wordt het jaar van release bewaard.
-	Releaseyear: wordt automatisch geupdate als een nieuw jaar start

7.	Sizes:
UITLEG: Deze tabel houdt maten bij van kledingstukken. Als het geen kledingstuk is, krijgt deze automatisch de waarde 99 “inapplicable”
-	Sizenr: Primary Key : vooraf ingesteld bij invoer gegevens
-	Size: Maat van het artikel

8.	Venues:
UITLEG: Deze tabel wordt enkel gebruikt bij een verkoop op locatie (op een show dus). Bedoeling is om zo te zien welke regio het best verkoopt.
-	venuenr: Primary Key :
-	venuename: Naam van de zaal waar de show doorgaat
-	Address : Spreekt voor zich
-	Postalcode : hoort bij adres
-	Location: hoort bij adres
-	Country: hoort bij adres

