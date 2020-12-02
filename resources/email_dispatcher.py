import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

log = logging.getLogger('__main__')

def send_email(emailTo, msg):
    sendStatus = False
    FROM = 'fontenayapp@gmail.com'
    TO = emailTo
    PASSWORD = 'f0nt3n4y4pp.'

    msg["From"] = FROM
    msg["To"] = TO

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(FROM, PASSWORD)
        server.sendmail(FROM, TO, msg.as_string())
        server.close()
        #log.error("\n\n\nEnvio: " + emailTo +"\n\n\n")
        sendStatus = True
    except:
        #log.error("\n\n\nFallo: " + emailTo +"\n\n\n")
        sendStatus = False
    return sendStatus



def prepare_sale_email(sale, sold_products):
    SUBJECT = 'Confirmacion de reserva'
    TEXT = 'Reserva exitosa'

    message = MIMEMultipart("alternative")
    message["Subject"] = SUBJECT

    # Create the plain-text and HTML version of your message
    text = """\
    TEXT"""
    html = """\
    <html>
        <head>
            <style>
                td.header {
                    border-bottom: 2px dashed black;
                    border-right: 2px dashed black;
                    border-top: 2px dashed black;
                }
                td.first {
                    border-left: 2px dashed black;
                }
				td.text-align-right {
					text-align: right;
				}
				.fondo-gris {
					background-color: lightgray;
					padding: 10px;
				}
				.letra-gris {
					color: lightgray;
					text-align: left;
				}
				.inline-block{
					display: inline-block;
				}
				body {
					font-family: "Helvetica Neue",Helvetica,Arial,sans-serif;
					width: 800px;
				}
				.font-size {
					font-size: 18px;
				}
				.voucher {
					font-size: 13px;
					text-align: justify;
					padding: 0 10px;
				}
				.vert-align {
					vertical-align: top;
				}
				table {
					width:100%
				}
				.container-div {
				    margin-bottom: 60px;
                    margin: 0 50px 60px;
                    border-bottom: 2px black solid;
                    width: 700px;
                }
                .logo {
                    margin: 5px -20px 0 10px;
                    height: 50px;
                    width: 225px;
                }
            </style>
        </head>
        <body>
            <a href="http://fontenay-staging.herokuapp.com/pages/voucher.html?saleid=""" + str(sale.sale_id) + """&download=true">
                <h2>Si lo desea, puede descargar su voucher en pdf haciendo click aquí</h2>
            </a>
        """
    #<a href="http://fontenay-staging.herokuapp.com/pages/voucher.html?saleid=""" + str(sale.sale_id) + """&download=true" target="_blank">Si lo desea, puede descargar su voucher en pdf haciendo click aquí</a>

    for sold_prod in sold_products:
        date = str(sold_prod.date)[8:10] + "/" + str(sold_prod.date)[5:7] + "/" + str(sold_prod.date)[:4]
        time = str(sold_prod.date)[-8:-3]
        html += """\
        <div class="container-div">
            <table>
                <tbody>
                    <tr>
                        <td class="header first"><img class="logo" src="https://fontenay.herokuapp.com/dist/images/logo.png"></td>
                        <td class="header">
                            <div>Número de solicitud de compra:</div>
                             <strong>3258537</strong></td>
                        <td class="header">
                             <div>Código de reserva / Reservation number:</div>
                             <strong>N°- """ + str(sold_prod.sold_product_id) + """</strong>
                        </td>
                    </tr>
                </tbody>
            </table>
            <table>
                <thead>
                    <tr>
                        <th><h5 class="letra-gris">Información de la reserva / Booking information</h5></th>
                        <th><h5 class="letra-gris">Información para el proveedor / Supplier information</h5></th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>
                            <h4 class= "font-size">""" + str(sold_prod.product.name) + """</h4>
                            <div>
                                <label><b>Fecha de la actividad / Tour date:</b></label>
                                <p class= "inline-block">""" + date + """</p>
                            </div>
                            <div>
                                <label><b>Retiro a nombre de:</b></label>
                                <p class= "inline-block">""" + str(sale.client.name) + """</p>
                            </div>
                            <div>
                                <label><b>Pick-up:</b></label>
                                <p class= "inline-block">Desde """ + time + """hs. a 30 min. después.</p>
                            </div>
                            <div>
                                <label><b>Hotel:</b></label>
                                <p class= "inline-block">""" + str(sale.client.hotel) + """ (""" + str(sale.client.address) +""")</p>
                            </div>
                            <div>
                                <label><b>Habitación:</b></label>
                                <p class= "inline-block">""" + str(sale.client.room_number) + """</p>
                            </div>
                        </td>
                        <td class="vert-align">
                            <div class="fondo-gris">
                                <div>
                                    <label><b>Actividad / Activity:</b></label>
                                    <p class="inline-block">""" + str(sold_prod.product.name) + """</p>
                                </div>
                                <div>
                                    <label><b>Pasajeros / Travelers:</b></label>
                                    <p class="inline-block">Adultos: """ + str(sold_prod.adults) + """, Niños: """ + str(sold_prod.children) + """, Bebés: """ + str(sold_prod.babies) + """ </p>
                                </div>
                                <div>
                                    <label><b>Empresa / Company:</b></label>
                                    <p class="inline-block">""" + str(sold_prod.product.provider.name) +"""</p>
                                </div>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
            <h4 class="fondo-gris font-size">Instrucciones y datos de contacto </h4>
            <p class= "voucher">
                En caso de emergencia, comunicarse con Fontenay Tours<br>
                Mail: fontenaytours@gmail.com<br>
                Teléfono: +54 11 4893 0771 / +54 11 68388892 (WhatsApp)
            </p>
            <p class= "voucher">
                Dada la Ley Civil de Argentina, Fontenay no es responsable de los sucesos provocados por terceros, fuerza mayor y eventos de la naturaleza.
            </p>
            <p class= "voucher">
                No se responsabiliza de viaje opcional vendido en cada lugar. Ninguno de nuestros guías y/o controladores están autorizados a revender estos opcionales. Las guías y los conductores son capaces de simplemente orientar e informar a los clientes sobre las atracciones locales (ejemplos: paseos, restaurantes y otros). Para su seguridad, si usted quiere comprar un tour o una transferencia, haga contacto directo con el centro de Fontenay Tours.
            </p>
            <p class= "voucher">
                Las pertenencias de mano transportados en el vehículo son responsabilidad del pasajero y no están sujetos a ningún tipo de indemnización por daños o pérdidas. (De acuerdo con la Resolución 1432, párrafo 6, el artículo 8 26/04/2006 ANTT).
            </p>
            <h5><strong><b>Datos de contacto</b></strong></h5>
                <p class= "voucher">
                    Teléfonos:  +54 11 4893 0771 / +54 11 6838 8892<br>
                    Correo electrónico: fontenaytours@gmail.com<br>
                    Dirección: Av. Cordoba 543, Galeria Buenos Aires, Escritorio “74”
                </p>
            <h4 class= "font-size"><strong><b>Políticas de cancelación</b></strong></h4>
                <p class= "voucher">Puede realizar la cancelación sin cargo hasta 24hs. antes de iniciar la actividad (excepto actividades internacionales). Para más información, consulte las políticas de cancelación en nuestra página web.</p>
            <table>
                <tbody>
                    <tr>
                        <td><strong>Imprima este voucher</strong></td>
                        <td class="text-align-right">Imprima este voucher y llévelo con usted en su viaje.</td>
                    </tr>
                </tbody>
            </table>
        </div>
        """
    html += """\
        </body>
    </html>
    """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    return message



def prepare_provider_email(prod, sale):
    SUBJECT = 'Reserva de servicios'
    TEXT = 'Reservar de servicio.'

    message = MIMEMultipart("alternative")
    message["Subject"] = SUBJECT

    dt = prod.get('date')
    date = str(dt)[8:10] + "/" + str(dt)[5:7] + "/" + str(dt)[:4] + " a las " + str(dt)[-8:-3] + "hs."

    text = """\
    TEXT"""
    html = """\
    <html>
      <body>
        <p>Estimados,<br>
        Un gusto saludarlos.<br>
        Les solicito la siguiente reserva:<br>
        </p>
        <ul>
            <li>Fecha y hora: """ + date + """ </li>
            <li>Servicio:  """ + str(prod.get('product').get('name')) + """ </li>
            <li>Cliente: """ + str(sale.client.name) + """</li>
            <li>Adultos: """ + str(prod.get('adults')) + """, Niños: """ + str(prod.get('children')) + """, Bebés: """ + str(prod.get('babies')) + """</li>
            <li>Datos hospedaje:<br>
                <ul>
                    <li>Hotel: """ + str(sale.client.hotel) + """</li>
                    <li>Dirección: """ + str(sale.client.address) + """</li>
                    <li>Habitación: """ + str(sale.client.room_number) + """</li>
                </ul>
            </li>
            <li>ID de venta: """ + str(sale.sale_id) + """</li>
        </ul>
        <p>Por favor, confirmar la reserva respondiendo a este mismo correo.<br>
        ¡Muchas gracias de antemano!</p><br><br>
        <h4>Fontenay Tours</h4>
      </body>
    </html>
    """


    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    return message



def prepare_receipt_email(sale, sold_products):
    SUBJECT = 'Recibo venta Fontenay'
    TEXT = 'Reservar de servicio.'

    message = MIMEMultipart("alternative")
    message["Subject"] = SUBJECT

    date = str(sale.date)[8:10] + "/" + str(sale.date)[5:7] + "/" + str(sale.date)[:4]

    text = """\
    TEXT"""
    html = """\
    <html>
    	<head>
    		<style>
    		body {
    			font-family: "Helvetica Neue",Helvetica,Arial,sans-serif;
    			font-size: 14px;
    		}
    		#total-width {
    			width: 800px;
    			padding: 25px;
    		}
    		.first-col-width {
    			width: 450px;
    		}
    		.half-first-col-width {
    			width: 210px;
    		}
    		.second-col-width {
    			max-width: 350px;
    			min-width: 200px;
    		}
    		.align-text {
    			text-align: left;
    		}
    		.striped>tbody>tr:nth-of-type(odd) {
    			background-color: #eee;
    		}
    		th, td {
    			padding: 5px;
    		}
    		table {
    			font-size: 14px;
    			border-collapse: collapse;
    		}
    		#gray-border {
    			border-bottom: #ccc solid 2px;
    		}
    		.logo {
                margin: 5px -20px 0 10px;
                height: 50px;
                width: 225px;
            }
    		</style>
    	</head>
        <body>
            <div id="total-width">
                <div class="header first">
                    <img class="logo" src="https://fontenay.herokuapp.com/dist/images/logo.png">
                </div>
                <table>
                    <tbody>
                        <tr>
                            <td class= "first-col-width"> Av. Córdoba 543, local 74.</td>
                            <td class="second-col-width">N° de formato:</td>
                        </tr>
                        <tr>
                            <td class= "first-col-width"> CP 1054, CABA.</td>
                            <td class="second-col-width"> """ + str(sale.sale_id) + """</td>
                        </tr>
                        <tr>
                            <td class= "first-col-width"> Ciudad Autónoma de Buenos Aires, Argentina.</td>
                            <td class="second-col-width">Fecha del formato:<br> """ + date + """</td>
                        </tr>
                        <tr>
                            <td class= "first-col-width"> Número de identificación fiscal: 16.426</td>
                            <td class="second-col-width">Cliente:<br> """ + str(sale.client.name) + """</td>
                        </tr>
                        <tr>
                            <td class= "first-col-width"><p>
                            Teléfono: +54 11 68388892<br>
                            Lunes a Viernes, de 9:00hs. a 18:00hs.<br>
                            fontenaytours@gmail.com<br>
                            www.fontenaytours.com<br>
                            </p></td>
                            <td class="second-col-width">Email:<br>""" + str(sale.client.email) + """</td>
                        </tr>
                    </tbody>
                </table><br><br>
                <table class="striped">
                    <thead id="gray-border">
                        <tr>
                            <th class= "align-text first-col-width">Descripción</th>
                            <th class= "align-text second-col-width">Cantidad personas</th>
                        </tr>
                    </thead>
                    <tbody>
                    """

    for sold_prod in sold_products:
        html += """\
                        <tr>
                            <td>""" + str(sold_prod.product.name) + """</td>
                            <td>""" + str(sold_prod.adults + sold_prod.children + sold_prod.babies) + """</td>
                        </tr>
        """
    html += """\
                    </tbody>
                </table><br><br>
                <table>
                    <thead>
                        <tr>
                            <th class="align-text half-first-col-width"><b>Subtotal</b></th>
                            <th class="align-text half-first-col-width"><b>Descuento</b></th>
                            <th class="align-text"><b>TOTAL</b></th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>ARS $""" + str(format(sale.total + sale.discount, '.2f')) + """</td>
                            <td>ARS $""" + str(format(sale.discount, '.2f')) + """</td>
                            <td><b>ARS $""" + str(format(sale.total, '.2f')) + """</b></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </body>
    </html>
    """


    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    return message
