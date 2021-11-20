import smtplib
import humidityTemperatureData

def sendDistanceError(distance, numSounds):
    smtpUser    = 'Rasp.Pi4201@Gmail.com'
    smtpPass    = 'EE42013mb3d!'

    toAdd       = 'Rasp.Pi4201@Gmail.com'
    fromAdd     = smtpUser

    # temperature_c, temperature_f, humidity = humidityTemperatureData.getTempandHumidity()

    subject     = 'Distance ALERT Information'
    header      = 'To:' + toAdd + '\n' + 'From:' + fromAdd + '\n' + 'Subject:' + subject
    body        = f'Alarm has been turned off!\nDistance = {distance}cm\nNumber of attempts to wakeup = {numSounds}'
    # print(header + '\n' + body)

    server = smtplib.SMTP('smtp.gmail.com', 587)

    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login(smtpUser, smtpPass)
    print("Login Successful!")

    server.sendmail(fromAdd, toAdd, header + '\n\n' + body)
    print(f"Distance Error Sent to {toAdd} from {smtpUser}")

    server.quit()