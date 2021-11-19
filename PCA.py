import cv2
from pyzbar import pyzbar
from datetime import datetime


def ler_qrcode(frame):
    qr_code = pyzbar.decode(frame)

    for qr in qr_code:
        x, y, w, h = qr.rect

        # Definindo a decodificação do QRcode
        qr_info = qr.data.decode('utf-8')
        # Definindo o retangulo ao redor do QRcode
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 0), 2)
        # Adicionando texto ao retangulo > Definindo a fonte
        fonte = cv2.FONT_HERSHEY_DUPLEX
        # Definindo localização do texto, cor e expessura
        cv2.putText(frame, qr_info, (x + 6, y - 6), fonte, 2.0, (26, 0, 255), 1)
        # Criando arquivo para armazenar informações do QRcode

        data = datetime.today()
        hora = datetime.now()
        data = data.strftime('%d/%m/%Y')
        hora = hora.strftime("%H:%M")

        with open("historico.txt", "a+") as file:
            file.write(qr_info + ',' + data + ',' + hora + "\n \r")

    return frame


def removedups(inputfile, outputfile):
    lines = open(inputfile, 'r').readlines()
    lines_set = set(lines)
    out = open(outputfile, 'w')
    for line in lines_set:
        if line.isspace():
            pass
        else:
            out.write(line)


def separar(inputfile):
    cols = ['Produto', 'Data', 'Hora']
    novos_dados = ''
    with open(inputfile) as f:
        for l in f:  # o slice vai ser feito na linha abaixo para cada linha
            novos_dados += '{};{};{};\n'.format(l[:8], l[9:19], l[20:25])
    content = '{}\n{}'.format(';'.join(cols), novos_dados)

    # gravar content em um csv
    print(content, file=open('novos_dados.csv', 'w'))
    print(novos_dados)


def main():
    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()

    while ret:
        ret, frame = camera.read()
        frame = ler_qrcode(frame)
        removedups('historico.txt', 'codigos_unicos.txt')
        nome_janela = 'leitor de QRcode'
        cv2.namedWindow(nome_janela, cv2.WINDOW_NORMAL)
        cv2.setWindowProperty(nome_janela, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow(nome_janela, frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    camera.release()
    cv2.destroyAllWindows()
    separar('codigos_unicos.txt')


if __name__ == '__main__':
    main()
