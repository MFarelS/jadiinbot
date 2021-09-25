const express = require('express')
const http = require('http')
const { Server } = require("socket.io")
const qrcode = require("qrcode")
const axios = require('axios')
const { Session} = require('./models')
const WhatsappBot = require('./whatsapp-bot/index')

const config = {
    port: 3000,
    api_url: 'http://127.0.0.1:8000/',
}

const connections = {

}
const connections_by_socket = {

}
const app = express()
const server = http.createServer(app)
const io = new Server(server);

io.on('connection', async (socket) => {
    socket.on('make_connection', async (data) => {
        const result = await axios.get(`${config.api_url}api/get-user-by-session?session_key=${data}`)
        const user_id = result.data.data.user
        const result_query = await Session.findOne({
            where: {
                owner_id: user_id,
            }
        })
        if (!result_query) {

            connections[user_id] = (new WhatsappBot()).conn
            connections_by_socket[socket.id] = connections[user_id]
            connections[user_id].version = [2, 2119, 6]
            connections[user_id].on('qr', async (qr) => {
                socket.emit('qr', await qrcode.toDataURL(qr))
            })
            connections[user_id].on('open', () => {
                socket.emit('open')
            })

            connections[user_id].on('open', async () => {
                const session = await Session.create({
                    session: JSON.stringify(connections[user_id].base64EncodedAuthInfo()),
                    owner_id: user_id
                })
                session.save()
            })

            connections[user_id].connect()

        }
    })

    socket.on('close_connection', async (data) => {
        const result = await axios.get(`${config.api_url}api/get-user-by-session?session_key=${data}`)
        const user_id = result.data.data.user
        const result_query = await Session.findOne({
            where: {
                owner_id: user_id,
            }
        })
        if (result_query) result_query.destroy()
        if (connections[user_id]) {
            connections[user_id].logout()
            connections[user_id].close()
        }
    })

    socket.on('disconnect', () => {
        if (connections_by_socket[socket.id] && !connections_by_socket[socket.id].user) {
            connections_by_socket[socket.id].close()
        }
    })

})

app.get('/conn/:conn_id', (req, res) => {
    const response = {}
    const conn = connections[req.params.conn_id]
    if (!conn) {
        response.msg = 'not found'
        res.json(response)
    } else {
        response.msg = 'ok'
        response.data = conn.user
        res.json(response)
    }
})


server.listen(config.port, async () => {
    const sessions = await Session.findAll()
    sessions.forEach(async (session) => {
        const conn = (new WhatsappBot()).conn
        conn.version = [2, 2119, 6]
        conn.loadAuthInfo(JSON.parse(session.dataValues.session))
        try {
            await conn.connect()
            connections[session.dataValues.owner_id] = conn
        } catch(e) {
            const ses = await Session.findOne({
                where: {
                    owner_id: session.dataValues.owner_id,
                }
            })
            ses.destroy()
        }
    })

    console.log("Server dimulai!")
})
