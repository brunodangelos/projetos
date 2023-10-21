const qrcode = require('qrcode-terminal');
const { Client, LocalAuth, MessageMedia } = require('whatsapp-web.js');
const express = require('express');
const multer = require('multer');
const moment = require('moment-timezone');

const app = express();
const port = 4000;

var http = require('http');
http.get({hostname: 'web.whatsapp.com'}, function(res) {
  console.log('A conexão com o site web.whatsapp.com foi bem-sucedida. Continuando a execução do programa...');
    const client = new Client({
      authStrategy: new LocalAuth(),
      puppeteer: { args: ['--no-sandbox'] }
  });

  client.on('qr', qr => {
      qrcode.generate(qr, {small: true});
  });

  client.initialize();

  client.on('loading_screen', (percent, message) => {
      console.log('Carregando', percent, message);
  });

  client.on('authenticated', () => {
      console.log('Autenticado');
  });

  client.on('auth_failure', msg => {
      // Fired if session restore was unsuccessful
      console.error('Falha na autenticacao', msg);
  });

  client.on('ready', () => {
      console.log('Cliente iniciado e pronto para uso!');

      // Inicialize o segundo script aqui
      app.use(express.json());
      app.use(express.urlencoded({ extended: true }));

      // Enviando mensagens inicio | POST //

      // Rota para enviar mensagem
      app.post('/api/message', (req, res) => {
        const { number, message } = req.body;

        const isGroup = (number) => {
          return number.toString().startsWith('55') && number.toString().length === 12 || number.toString().length === 13;
        };

        const getCurrentTime = () => {
            return moment().tz('America/Sao_Paulo').format('YYYY-MM-DD HH:mm:ss');
        };

        if (isGroup(number)) {

          // Envia a mensagem usando o cliente do WhatsApp
          client.sendMessage(`${number}@c.us`, message)
            .then(() => {
                // Registro de sucesso
                console.log(getCurrentTime(), '- Mensagem enviada com sucesso para:', number);
                //console.log('Mensagem:', message);
              res.json({ message: 'Mensagem enviada com sucesso' });
            })
            .catch((error) => {
                // Registro de erro
                console.error(getCurrentTime(), '- Erro ao enviar mensagem para:', number);
                console.error('Erro:', error);
              res.status(500).json({ error: 'Erro ao enviar mensagem' });
            });
        }
        else {

          // Envia a mensagem usando o cliente do WhatsApp
          client.sendMessage(`${number}@g.us`, message)
            .then(() => {
                // Registro de sucesso
                console.log(getCurrentTime(), '- Mensagem enviada com sucesso para:', number);
                //console.log('Mensagem:', message);
              res.json({ message: 'Mensagem enviada com sucesso' });
            })
            .catch((error) => {
                // Registro de erro
                console.error(getCurrentTime(), '- Erro ao enviar mensagem para:', number);
                console.error('Erro:', error);
              res.status(500).json({ error: 'Erro ao enviar mensagem' });
            });
        }

      });

      // Enviando mensagens fim | POST //

      // Enviando mensagens inicio | GET //

      // Rota para enviar mensagem
      app.get('/api/message', (req, res) => {
        const { number, message } = req.query;

        const isGroup = (number) => {
          return number.toString().startsWith('55') && number.toString().length === 12 || number.toString().length === 13;
        };

        const getCurrentTime = () => {
          return moment().tz('America/Sao_Paulo').format('YYYY-MM-DD HH:mm:ss');
        };

        if (isGroup(number)) {
          // Envia a mensagem usando o cliente do WhatsApp
          client.sendMessage(`${number}@c.us`, message)
            .then(() => {
            // Registro de sucesso
            console.log(getCurrentTime(), '- Mensagem enviada com sucesso para:', number);
            //console.log('Mensagem:', message);
              res.json({ message: 'Mensagem enviada com sucesso' });
            })
            .catch((error) => {
              console.error('Erro ao enviar mensagem:', error);
              res.status(500).json({ error: 'Erro ao enviar mensagem' });
            });
        }
        else {
          // Envia a mensagem usando o cliente do WhatsApp
          client.sendMessage(`${number}@g.us`, message)
            .then(() => {
                // Registro de sucesso
                console.log(getCurrentTime(), '- Mensagem enviada com sucesso para:', number);
                //console.log('Mensagem:', message);
                res.json({ message: 'Mensagem enviada com sucesso' });
            })
            .catch((error) => {
                // Registro de erro
                console.error(getCurrentTime(), '- Erro ao enviar mensagem para:', number);
                console.error('Erro:', error);
              res.status(500).json({ error: 'Erro ao enviar mensagem' });
            });
        }
      });

      // Enviando mensagens fim | GET //

      app.post('/api/download', upload.single('file'), async (req, res) => {

          const getCurrentTime = () => {
                  return moment().tz('America/Sao_Paulo').format('YYYY-MM-DD HH:mm:ss');
              };

          try {
              const {number, caption, base64image} = req.body;
              const media = MessageMedia('image/png', base64image);
              const isGroup = (number) => {
                return number.toString().startsWith('55') && number.toString().length === 12 || number.toString().length === 13;
              };

              if (isGroup(number)) {
                  await client.sendMessage(`${number}@c.us`, media, {caption: `${caption}`});
                  // Registro de sucesso
                  console.log(getCurrentTime(), '- Arquivo enviado com sucesso para:', number);
                  res.json({message: 'Arquivo enviado com sucesso para: ' + `${number}@c.us`});
              } else {
                  await client.sendMessage(`${number}@g.us`, media, {caption: `${caption}`});
                  console.log(getCurrentTime(), '- Arquivo enviado com sucesso para:', number);
                  res.json({message: 'Arquivo enviado com sucesso para: ' + `${number}@g.us`});
              }
          } catch (error){
              console.error(getCurrentTime(), '- Erro ao enviar o arquivo:', error);
              res.status(500).send('Erro ao enviar o arquivo');
          }
      });

      // Enviando arquivo fim //

      // Inicia o servidor
      app.listen(port, () => {
        console.log(`Servidor está rodando em http://localhost:${port}`);
      });
  });
}).on('error', function(e) {
  console.error('A conexão com o site web.whatsapp.com falhou. Encerrando a execução do programa...');
  process.exit(1);
});
