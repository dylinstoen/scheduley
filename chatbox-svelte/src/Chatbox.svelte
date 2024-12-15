<script>
  import {marked} from "marked";
    let chats = [];
    let activeChat = null;
    let messages = [];
    let userInput = "";
    let botTyping = false;
  
    const createNewChat = () => {
      const newChat = { title: `Chat ${chats.length + 1}`, messages: [] };
      chats = [...chats, newChat];
      switchChat(chats.length - 1);
    };

    const switchChat = (index) => {
      activeChat = index;
      messages = chats[index].messages;
    };
    const sendMessage = async () => {
      if (userInput.trim() && activeChat !== null) {
        const userMessage = { sender: "user", text: userInput };
        chats[activeChat].messages = [...chats[activeChat].messages, userMessage];
        messages = chats[activeChat].messages;
        const userInputText = userInput;
        userInput = "";
        await fetchAIResponse(userInputText);
      }
    };
  
    const fetchAIResponse = async (userInputText) => {
      botTyping = true;
      try {
        const response = await fetch("http://localhost:5001/api/chat", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({ message: userInputText })
        });

        const data = await response.json();

        if (data.response) {
          const botMessage = {
            sender: "bot",
            text: data.response
          };
          chats[activeChat].messages = [...chats[activeChat].messages, botMessage];
          messages = chats[activeChat].messages;
        } else {
          throw new Error(data.error || "Unexpected error");
        }
      } catch (error) {
        console.error("Error fetching AI response:", error);
        const errorMessage = {
          sender: "bot",
          text: "Sorry, there was an error processing your request. Please try again."
        };
        chats[activeChat].messages = [...chats[activeChat].messages, errorMessage];
        messages = chats[activeChat].messages;
      } finally {
        botTyping = false;
      }
    };

    const deleteChat = (index) => {
      chats = chats.filter((_, i) => i !== index);
      if (activeChat === index) {
        activeChat = null;
        messages = [];
      } else if (activeChat > index) {
        activeChat -= 1;
      }
    };
  </script>
<div class="chat-app">
    <div class="sidebar">
      <div class="chat-list">
        {#each chats as chat, index}
          <div
            class="chat-item {activeChat === index ? 'active' : ''}"
            on:click={() => switchChat(index)} on:keydown
          >
            <span>{chat.title}</span>
            <button class="delete-button" on:click={(e) => { e.stopPropagation(); deleteChat(index); }}>×</button>
          </div>
        {/each}
      </div>
      <button class="new-chat" on:click={createNewChat}>+ New Chat</button>
    </div>
  
    <div class="chatbox">
      {#if activeChat !== null}
        <div class="messages">
          {#each messages as { sender, text }}
            <div class="message-container {sender}">
              <div class="message {sender}">
                {@html marked(text)}
              </div>
            </div>
          {/each}
          {#if botTyping}
            <div class="bot-typing">Bot is typing...</div>
          {/if}
        </div>
        <div class="input-container">
          <input
            type="text"
            placeholder="Type a message..."
            bind:value={userInput}
            on:keypress={(e) => e.key === "Enter" && sendMessage()}
          />
          <button on:click={sendMessage}>Send</button>
        </div>
      {:else}
        <div class="messages">
          <p style="text-align: center; color: #888;">Select or create a new chat to start messaging.</p>
        </div>
      {/if}
    </div>
  </div>

  <style>
    .chat-app {
      display: flex;
      height: 500px;
      max-width: 800px;
      margin: auto;
      border: 1px solid #ccc;
      border-radius: 10px;
      box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
      background-color: #fff;
    }
  
    .sidebar {
      width: 200px;
      border-right: 1px solid #ccc;
      padding: 10px;
      background-color: #f9f9f9;
      display: flex;
      flex-direction: column;
    }
  
    .chat-list {
      flex-grow: 1;
      overflow-y: auto;
      margin-bottom: 10px;
    }
  
    .chat-item {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 8px;
      margin-bottom: 5px;
      border-radius: 5px;
      cursor: pointer;
      background-color: #e1e1e1;
    }
  
    .chat-item.active {
      background-color: #007bff;
      color: #fff;
    }
  
    .delete-button {
      background: none;
      border: none;
      color: #ff4d4d;
      font-size: 16px;
      cursor: pointer;
    }
  
    .delete-button:hover {
      color: #ff1a1a;
    }
  
    .new-chat {
      padding: 10px;
      background-color: #007bff;
      color: #fff;
      border: none;
      border-radius: 5px;
      cursor: pointer;
      text-align: center;
    }
  
    .new-chat:hover {
      background-color: #0056b3;
    }

    .chatbox {
      flex-grow: 1;
      display: flex;
      flex-direction: column;
    }
  
    .messages {
      flex-grow: 1;
      padding: 10px;
      overflow-y: auto;
      background-color: #f9f9f9;
    }
  
    .message-container {
      display: flex;
      margin: 5px 0;
    }
  
    .message-container.user {
      justify-content: flex-end;
    }
  
    .message-container.bot {
      justify-content: flex-start;
    }
  
    .message {
      padding: 10px;
      border-radius: 10px;
      max-width: 70%;
      word-wrap: break-word;
    }
  
    .message.user {
      background-color: #d1e7ff;
      text-align: right;
    }
  
    .message.bot {
      background-color: #f1f1f1;
      text-align: left;
    }
  
    .input-container {
      display: flex;
      border-top: 1px solid #ccc;
      padding: 10px;
      background-color: #fff;
    }
  
    .input-container input {
      flex-grow: 1;
      border: 1px solid #ccc;
      border-radius: 5px;
      padding: 10px;
      font-size: 14px;
    }
  
    .input-container button {
      margin-left: 10px;
      padding: 10px 15px;
      border: none;
      border-radius: 5px;
      background-color: #007bff;
      color: #fff;
      font-size: 14px;
      cursor: pointer;
    }
  
    .input-container button:hover {
      background-color: #0056b3;
    }
  </style>
  
 
  