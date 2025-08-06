export const chatInterfaceBlock = {
  name: "chat-interface",
  author: "n.Gabi Team (https://ngabi.ness.tec.br)",
  title: "Chat Interface",
  description: "A modern chat interface with AI agents, featuring real-time messaging, agent selection, and processing status indicators.",
  type: "registry:block",
  registryDependencies: [
    "card",
    "button", 
    "input",
    "select",
    "scroll-area",
    "badge",
    "avatar",
    "separator",
    "tooltip",
    "progress"
  ],
  dependencies: ["lucide-react"],
  files: [
    {
      path: "blocks/chat-interface/page.tsx",
      type: "registry:page",
      target: "app/chat/page.tsx",
    },
    {
      path: "blocks/chat-interface/components/chat-interface.tsx",
      type: "registry:component",
    },
    {
      path: "blocks/chat-interface/hooks/use-chat.ts",
      type: "registry:hook",
    },
    {
      path: "blocks/chat-interface/lib/utils.ts",
      type: "registry:lib",
    },
  ],
  categories: ["chat", "ai", "interface"],
} 