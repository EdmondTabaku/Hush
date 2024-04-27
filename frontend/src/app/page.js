"use client";

import styles from "./page.module.css";
import {useEffect, useState} from "react";
import {IconButton, Input, Textarea} from "@mui/joy";
import SendIcon from '@mui/icons-material/Send';
import {Snackbar} from "@mui/joy";
import {encryptMessage, decryptMessage} from "@/util/encrypt";

export default function Home() {
  const [messages, setMessages] = useState([]);
  const [lastMsgLength, setLastMsgLength] = useState(0);
  const [client_id, setClient_id] = useState("");
  const [key, setKey] = useState("");
  const [message, setMessage] = useState("");
  const [receiverId, setReceiverId] = useState("");

  const [isAlertOpen, setIsAlertOpen] = useState(false);
  const [alertMessage, setAlertMessage] = useState('');
  const [alertType, setAlertType] = useState('danger');

  const backend = process.env.NEXT_PUBLIC_XPRESS_API_URL || "http://localhost:7000";

  useEffect(() => {
    // Get the client_id and key from the local storage
    const client_id = localStorage.getItem("client_id");
    const key = localStorage.getItem("key");
    const checkClient = async () => {

      const isValid = await isClientValid(client_id, key);

      if (client_id && key && isValid === true){
          setClient_id(client_id);
          setKey(key);
      } else {
          getClient();
      }
    }

    getMessages(client_id, key);

    checkClient();
  }, []);

  useEffect(() => {
      const intervalId = setInterval(() => {
        getMessages(client_id, key);
      }, 2000); // 3000 milliseconds = 3 seconds

      // Cleanup function to clear the interval when the component unmounts
      return () => clearInterval(intervalId);
  }, [client_id, key]);

  useEffect(() => {
      setLastMsgLength(messages.length);
      if (messages.length > lastMsgLength) {
          const lastMsgElement = document.getElementById("last-msg");
          if (lastMsgElement) {
              lastMsgElement.scrollIntoView();
          }
      }
  }, [messages]);

  const getClient = async () => {
    const res = await fetch(`${backend}/client`);
    const data = await res.json();
    setClient_id(data.data.client_id);
    setKey(data.data.key);

    // Save the client_id and key to the local storage
    localStorage.setItem("client_id", data.data.client_id);
    localStorage.setItem("key", data.data.key);
  }

  const isClientValid = async (client_id, key) => {
    const res = await fetch(`${backend}/client/${client_id}/${key}`)
    const data = await res.json();
    if (data.status === 200) {
        if (data.data.is_valid === true) {
            return true;
        }
    }
    return false;
  }

  const getMessages = async (client_id, key) => {
    const res = await fetch(`${backend}/message?client_id=${client_id}&key=${key}`);
    const data = await res.json();
    if (data.status === 200) {
        // Decrypt the messages
        const decryptedMessages = data.data.map(msg => {
            return {
                ...msg,
                message: decryptMessage(msg.message, msg.iv, msg.sender_id)
            }
        });
        setMessages(decryptedMessages);
    }
  }

  const sendMessage = async (sender_id, key, receiverId, message) => {
    const { iv, encryptedMessage } = encryptMessage(message, sender_id);
    const res = await fetch(`${backend}/message/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
      },
      body: JSON.stringify({
        sender_id: sender_id,
        key: key,
        receiver_id: receiverId,
        message: encryptedMessage,
        iv: iv
      }),
    });
    const data = await res.json();
    if (data.status === 200) {
        setAlertMessage("Message sent successfully!");
        setAlertType("success");
        setIsAlertOpen(true);
        setMessage("");
    } else {
        setAlertMessage("Failed to send message!");
        setAlertType("danger");
        setIsAlertOpen(true);
    }
  }

  return (
    <main className={styles.main}>
      <h1>{client_id}</h1>
      <div className={styles.container}>
          <div className={styles.messages}>
              {messages.map((msg, index) => (
                  <div key={msg.id} className={styles.message} id={index === messages.length - 1 ? "last-msg" : ""}>
                      <div className={styles.msgHeader}>
                          <p className={styles.sender}>{msg.sender_id}</p>
                          <p className={styles.time}>{new Date(msg.created_at * 1000).toLocaleString()}</p>
                      </div>
                      <p className={styles.msgText}>{msg.message}</p>
                  </div>
              ))}
          </div>
          <div className={styles.send}>
              <div className={styles.sendHeader}>
                  <Input
                      placeholder="Receiver ID"
                      variant="solid"
                      value={receiverId.toUpperCase()}
                      onChange={(e) => setReceiverId(e.target.value)}
                      sx={{
                          backgroundColor: "#232323",
                          color: "#fff",
                          maxWidth: "150px",
                          maxHeight: "38px",
                          textTransform: "uppercase"
                      }}
                  ></Input>
                  <Textarea
                      className={styles.textarea}
                      placeholder="Type the message..."
                      variant="solid"
                      value={message}
                      onChange={(e) => setMessage(e.target.value)}
                      sx={{
                          backgroundColor: "#232323",
                          color: "#fff",
                          width: "100%",
                      }}
                  />
              </div>
              <IconButton
                  className={styles.sendButton}
                  sx={{
                      backgroundColor: "#232323",
                      color: "#fff",
                      maxHeight: "38px",
                      '&:hover': {
                          backgroundColor: "#3d3d3d",
                          color: "#e0e0e0",
                      }
                  }}
                  onClick={() => sendMessage(client_id, key, receiverId, message)}
              >
                  <SendIcon
                      sx={{
                          transform: "rotate(-90deg)",
                      }}
                  />
              </IconButton>
          </div>
          <p className={styles.end}>All messages are end-to-end encrypted</p>
      </div>
        <Snackbar
            open={isAlertOpen}
            onClose={() => setIsAlertOpen(false)}
            variant="solid"
            color={alertType}
            autoHideDuration={6000}
        >
            {alertMessage}
        </Snackbar>
    </main>
  );
}
