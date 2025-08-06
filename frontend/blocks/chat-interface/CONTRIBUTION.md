# Chat Interface Block - Contribution to shadcn/ui

## Overview

This block provides a complete chat interface solution for AI applications, featuring modern design patterns and best practices for real-time messaging.

## What's Included

### Components
- **ChatInterface**: Main component with full chat functionality
- **ChatMessage**: Individual message component with avatars and timestamps

### Hooks
- **useChat**: Custom hook for managing chat state and message handling

### Utils
- **formatTimestamp**: Time formatting utility
- **generateMessageId**: Unique ID generation for messages
- **truncateText**: Text truncation utility

## Key Features

1. **Modern Design**: Clean, accessible interface with proper spacing and typography
2. **Agent Selection**: Dropdown to switch between different AI assistants
3. **Real-time Feedback**: Processing status indicators and loading states
4. **Responsive**: Works perfectly on all screen sizes
5. **Dark Mode**: Full support for light and dark themes
6. **Accessible**: Proper ARIA labels and keyboard navigation
7. **TypeScript**: Full type safety throughout

## Technical Highlights

- Uses 10+ shadcn/ui components for consistency
- Implements proper state management with React hooks
- Follows modern React patterns and best practices
- Includes comprehensive TypeScript types
- Provides excellent developer experience

## Installation Requirements

```bash
npx shadcn@latest add card button input select scroll-area badge avatar separator tooltip progress
```

## Usage Example

```tsx
import { ChatInterface } from './components/chat-interface'
import { useChat } from './hooks/use-chat'

function App() {
  const { messages, sendMessage, isLoading, selectedAgent, setSelectedAgent } = useChat()
  
  return (
    <ChatInterface
      messages={messages}
      onSendMessage={sendMessage}
      isLoading={isLoading}
      selectedAgent={selectedAgent}
      onAgentChange={setSelectedAgent}
    />
  )
}
```

## Why This Block?

This block solves common challenges in building chat interfaces:
- Complex state management for messages
- Real-time feedback for user actions
- Agent switching functionality
- Proper message formatting and display
- Loading states and error handling

## Community Impact

This block will help developers quickly implement professional chat interfaces in their applications, reducing development time and ensuring consistent, high-quality user experiences.

## License

MIT License - open for community use and modification. 