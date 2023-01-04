# import wszystkich niezbędnych bibliotek

import numpy as np
import matplotlib.pyplot as plt
import time, random, smtplib, imghdr, os
from email.message import EmailMessage

# inicjacja zmiennych charakteryzujących dany pomiar

date = time.strftime('%Y_%m_%d_%H_%M_%S')
analogValue = 0
analogArray = []
freq = 0.5
fullTime = 5
xAxis = np.arange(0, fullTime+freq, freq)

# logika przliczania symulacji pomiaru analogowego na wartość w gramach

for i in xAxis:
    analogValue = random.randint(0, 65535) # symulacja sygnału z kontrolera

    if analogValue >= 0 and analogValue < 17964:
        mass = analogValue / 183.31
    elif analogValue >= 17964 and analogValue < 36554:
        mass = (analogValue - 15937.5) / 20.68
    elif analogValue >= 36554 and analogValue <= 65535:
        mass = (analogValue - 28305.63) / 8.27

    analogArray.append(mass)
    time.sleep(freq)

# rysowanie wykresu i zapisanie go korzystając z biblioteki matplotlib

plt.xlabel('time [s]')
plt.ylabel('mass [g]')
plt.plot(xAxis, analogArray)
plt.savefig('TrainingGraph{}.jpg'.format(date))

# decyzja o wysłaniu maila / wyświetleniu wykresu / zakończenia działania aplikacji

temp = input('Type y/n to send email or just show the created graph\n')

if temp.lower() == 'y':
    firstName = 'Bartłomiej'
    lastName = 'Ciupka'

# definicja zmiennych użytych do stworzenia obiektu EmailMessage

    mailFrom = 'bartek.ciupka@gmail.com'
    mailTo = 'bartek.ciupka@gmail.com'
    mailSubject = 'Analiza treningowa: {} {} - {}'.format(firstName, lastName, date)
    mailBody = '''Imię pacjenta: {}
Nazwisko pacjenta: {}
Data wykonania treningu: {}'''.format(firstName, lastName, date)

    user = 'bartek.ciupka@gmail.com'
    password = os.environ.get('GMAILPASS') # hasło pobierane ze zmiennych środowiskowych (niewidoczne)

    path = r'./TrainingGraph{}.jpg'.format(date)

# parametryzacja obiektu EmailMessage

    message1 = EmailMessage()
    message1['From'] = mailFrom
    message1['Subject'] = mailSubject
    message1['To'] = mailTo
    message1.set_content(mailBody)

# otworzenie bitowe pliku .img z wykresem i zapisanie w zmiennych jego parametrów

    with open(path, 'rb') as f:
        file = f.read()
        file_name = os.path.basename(path)
        file_type = imghdr.what(f.name)

    # dodanie załącznika w postaci wykresu do obiektu EmailMessage

    message1.add_attachment(file, maintype='image', subtype=file_type, filename=file_name)

# logowanie i wysyłanie maila z uproszczoną obsługą błędów

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=5) as server1:
            server1.login(user, password)
            server1.send_message(message1)
            print('Success!')
    except:
        print('Error during sending email')

# opcja z samym wyświetleniem wykresu

elif temp.lower() == 'n':
    plt.show()

# zakończenie programu w przypadku wprowadzenia innej litery

else:
    pass