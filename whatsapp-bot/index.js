const messageHandler = require("./messageHandler.js")
const { WAConnection } = require("@adiwajshing/baileys")

class WhatsappBot {
	constructor() {
		this.conn = new WAConnection()
		this.conn.version = [2, 2119, 6]

		this.conn.on("chat-update", async (message) => {
			try {
				if (!message.hasNewMessage) return
				message = message.messages.all()[0]
				if (!message.message || message.key.fromMe || message.key && message.key.remoteJid == 'status@broadcast') return
				if (message.message.ephemeralMessage) {
					message.message = message.message.ephemeralMessage.message
				}
				
				await messageHandler(this.conn, message)
			} catch(e) {
				console.log("[ERROR] " + e.message)
				this.conn.sendMessage(message.key.remoteJid, "Terjadi error! coba lagi nanti", "conversation", { quoted: message })
			}
		})

	}
}

module.exports = WhatsappBot
