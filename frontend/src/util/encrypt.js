const crypto = require('crypto');

function getKeyFromId(id) {
    // Hash the ID to derive a 256-bit key (for AES-256)
    return crypto.createHash('sha256').update(id).digest();
}

function encryptMessage(message, id) {
    const key = getKeyFromId(id);
    const iv = crypto.randomBytes(16); // Initialization vector for AES
    const cipher = crypto.createCipheriv('aes-256-cbc', key, iv);
    let encrypted = cipher.update(message, 'utf8', 'hex');
    encrypted += cipher.final('hex');
    return { iv: iv.toString('hex'), encryptedMessage: encrypted };
}

function decryptMessage(encrypted, iv, id) {
    const key = getKeyFromId(id);
    const decipher = crypto.createDecipheriv('aes-256-cbc', key, Buffer.from(iv, 'hex'));
    let decrypted = decipher.update(encrypted, 'hex', 'utf8');
    decrypted += decipher.final('utf8');
    return decrypted;
}

export { encryptMessage, decryptMessage };