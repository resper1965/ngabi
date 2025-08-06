# Chat Interface Block

A modern chat interface with AI agents, featuring real-time messaging, agent selection, and processing status indicators.

## Features

- **Real-time messaging** with user and AI agent messages
- **Agent selection** with dropdown to choose different AI assistants
- **Processing status** with progress indicators
- **Responsive design** that works on all screen sizes
- **Dark mode support** with adaptive colors
- **Accessible** with proper ARIA labels and keyboard navigation
- **TypeScript** support with full type safety

## Components

### ChatInterface
The main component that renders the complete chat interface.

```tsx
<ChatInterface
  messages={messages}
  onSendMessage={sendMessage}
  isLoading={isLoading}
  selectedAgent={selectedAgent}
  onAgentChange={setSelectedAgent}
/>
```

### ChatMessage
Individual message component with avatar, timestamp, and content.

```tsx
<ChatMessage message={message} />
```

## Hooks

### useChat
Custom hook for managing chat state and message handling.

```tsx
const { messages, sendMessage, isLoading, selectedAgent, setSelectedAgent } = useChat()
```

## Utils

### formatTimestamp
Formats a date into a readable time string.

```tsx
const time = formatTimestamp(new Date()) // "2:30 PM"
```

### generateMessageId
Generates a unique ID for messages.

```tsx
const id = generateMessageId() // "1703123456789abc123"
```

## Installation

This block requires the following shadcn/ui components:

```bash
npx shadcn@latest add card button input select scroll-area badge avatar separator tooltip progress
```

## Usage

1. Install the required dependencies
2. Copy the block files to your project
3. Import and use the components as needed

## Customization

The block is fully customizable through:
- CSS variables for theming
- Props for behavior modification
- Component composition for layout changes

## License

MIT License - feel free to use in your projects! 