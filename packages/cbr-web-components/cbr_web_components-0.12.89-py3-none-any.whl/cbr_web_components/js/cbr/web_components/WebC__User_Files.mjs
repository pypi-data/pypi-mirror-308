// WebC__User_Files.mjs
import Web_Component from '../../core/Web_Component.mjs'
import Div           from '../../core/Div.mjs'
import API__Invoke   from "../../data/API__Invoke.mjs";

export default class WebC__User_Files extends Web_Component {
    load_attributes() {
        this.add_css_rules(this.css_rules())
        this.api_invoke = new API__Invoke()
    }

    connectedCallback() {
        super.connectedCallback()
        this.build()
        this.add_event_listeners()
    }

    add_event_listeners() {
        // Tree refresh handler
        this.shadowRoot.addEventListener('files-refresh', () => {
            const tree_view = this.shadowRoot.querySelector('webc-user-files-tree-view')
            if (tree_view) { tree_view.refresh() }
        })

        // Folder selection handler - show folder viewer, hide file viewer
        // document.addEventListener('folder-selected', () => {
        //     const file_viewer   = this.shadowRoot.querySelector('webc-user-files-file-viewer')
        //     const folder_viewer = this.shadowRoot.querySelector('webc-user-files-folder-viewer')
        //
        //     if (file_viewer  ) { file_viewer.style.display   = 'none'  }
        //     if (folder_viewer) { folder_viewer.style.display = 'block' }
        // })
        //
        // // File selection handler - show file viewer, hide folder viewer
        // document.addEventListener('file-selected', () => {
        //     const file_viewer   = this.shadowRoot.querySelector('webc-user-files-file-viewer')
        //     const folder_viewer = this.shadowRoot.querySelector('webc-user-files-folder-viewer')
        //
        //     if (file_viewer  ) { file_viewer.style.display   = 'block' }
        //     if (folder_viewer) { folder_viewer.style.display = 'none'  }
        // })

        // Session change handler - reload all components
        document.addEventListener('active_session_changed', () => this.reload_all_components())

        document.addEventListener('file-selected', async (e) => {
            const file_viewer = this.shadowRoot.querySelector('webc-user-files-file-viewer')
            const folder_viewer = this.shadowRoot.querySelector('webc-user-files-folder-viewer')
            const chatbot = this.shadowRoot.querySelector('chatbot-openai')

            if (file_viewer) { file_viewer.style.display = 'block' }
            if (folder_viewer) { folder_viewer.style.display = 'none' }

            // Get file summary and update chat context
            const file_id = e.detail.node_id
            try {
                const response = await this.api_invoke.invoke_api(
                    `/api/user-data/files/file-contents?file_id=${file_id}`
                )
                console.log('File summary:', response?.data?.file_summary)
                if (response?.data?.file_summary) {
                    const system_prompt = `You are a helpful assistant discussing a file. Here is the file summary:
                        ${response.data.file_summary}
                        
                        Please help answer questions about this file and its contents.`

                    chatbot.system_prompt = system_prompt
                    chatbot.show_system_prompt = true
                    chatbot.initial_message = `I'm ready to discuss the file: ${e.detail.name}`
                    window.chatbot = chatbot
                }
            } catch (error) {
                console.error('Error loading file summary:', error)
            }
        })

        // Folder selection handler
        document.addEventListener('folder-selected', async (e) => {
            const file_viewer = this.shadowRoot.querySelector('webc-user-files-file-viewer')
            const folder_viewer = this.shadowRoot.querySelector('webc-user-files-folder-viewer')
            const chatbot = this.shadowRoot.querySelector('chatbot-openai')

            if (file_viewer) { file_viewer.style.display = 'none' }
            if (folder_viewer) { folder_viewer.style.display = 'block' }

            // Get folder summary and update chat context
            const folder_id = e.detail.node_id
            try {
                const path = `/api/user-data/file-to-llms/folder-summary?folder_id=${folder_id}&re_create=false`
                const response = await this.api_invoke.invoke_api(path, 'POST')

                if (response?.data) {
                    const system_prompt = `You are a helpful assistant discussing a folder and its contents. Here is the folder summary:
                        ${response.data}
                        
                        Please help answer questions about this folder and its contents.`

                    chatbot.system_prompt = system_prompt
                    chatbot.show_system_prompt = true
                    chatbot.initial_message = `I'm ready to discuss the folder: ${e.detail.name}`
                }
            } catch (error) {
                console.error('Error loading folder summary:', error)
            }
        })
    }
    reload_all_components() {
        // Refresh tree view
        const tree_view = this.shadowRoot.querySelector('webc-user-files-tree-view')
        if (tree_view) {
            tree_view.refresh()
        }

        // Refresh file viewer
        const file_viewer = this.shadowRoot.querySelector('webc-user-files-file-viewer')
        if (file_viewer) {
            file_viewer.clear_viewer?.() // Use optional chaining in case method doesn't exist
        }

        // Clear any active selections or states
        this.shadowRoot.querySelectorAll('.selected').forEach(element => {
            element.classList.remove('selected')
        })
    }
    build() {
        const container = new Div({ class: 'files-container' })

        // Left panel for tree view and actions
        const left_panel = new Div({ class: 'files-panel left-panel' })
        left_panel.add_tag({ tag: 'webc-user-files-tree-view' })
        left_panel.add_tag({ tag: 'webc-user-files-actions'   })
        left_panel.add_tag({ tag: 'webc-user-files-upload'    })

        // Right panel for file preview and chat
        const right_panel = new Div({ class: 'files-panel right-panel' })
        const preview_section = new Div({ class: 'preview-section' })
        preview_section.add_tag({ tag: 'webc-user-files-file-viewer'   })
        preview_section.add_tag({ tag: 'webc-user-files-folder-viewer' })

        const chat_section = new Div({ class: 'chat-section' })
        chat_section.add_tag({
            tag: 'chatbot-openai',
            attributes: {
                channel: 'files-chat',
                name: 'Files Assistant',
                edit_mode: 'false',
                url: '/api/llms/chat/completion',
                initial_message: 'Select a file or folder to discuss its contents.'
            }
        })

        right_panel.add_elements(preview_section, chat_section)
        container.add_elements(left_panel, right_panel)

        this.set_inner_html(container.html())
        this.add_event_listeners()
    }

    css_rules() {

        return {
            ":host"                : { display          : "block"                     ,            // Make component block level
                                     width             : "100%"                      ,            // Take full width
                                     height            : "100%"                      ,            // Take full height
                                     minHeight         : "0"                         },           // Allow content to shrink

            ".files-container"     : { display          : "flex"                      ,            // Main container as flex
                                     width             : "100%"                      ,            // Full width
                                     height            : "100%"                      ,            // Full height
                                     gap              : "1rem"                      ,            // Gap between panels
                                     padding          : "1rem"                      ,            // Padding around container
                                     backgroundColor  : "#f8f9fa"                   ,            // Light background
                                     position         : "absolute"                  ,            // Position absolute
                                     top              : "0"                         ,            // Align to top
                                     left             : "0"                         ,            // Align to left
                                     right            : "0"                         ,            // Stretch to right
                                     bottom           : "0"                         ,            // Stretch to bottom
                                     overflow         : "auto"                                  // Prevent overflow
                                    },

            ".files-panel"         : { //borderRadius     : "0.5rem"                   ,            // Rounded corners
                                       backgroundColor  : "#ffffff"                   ,            // White background
                                       //boxShadow        : "0 2px 4px rgba(0,0,0,0.1)" ,            // Subtle shadow
                                       overflow         : "hidden"                    ,            // Prevent overflow
                                       display          : "flex"                      ,            // Make panels flex containers
                                       flexDirection    : "column"                    },           // Stack children vertically

            ".left-panel"          : { width            : "350px"                     ,            // Fixed width for left panel
                                       minWidth         : "350px"                     ,            // Prevent shrinking below 350px
                                       display          : "flex"                      ,            // Flex for child elements
                                       flexDirection    : "column"                    ,            // Stack children vertically
                                       gap              : "1rem"                      ,            // Gap between components
                                       flexShrink       : "0"                         },           // Prevent shrinking

            ".right-panel"         : { flex             : "1 1 auto"                  ,            // Take remaining space
                                      minWidth         : "0"                         ,            // Allow shrinking
                                      display          : "flex"                      ,            // Make it flex container
                                      flexDirection    : "column"                    ,           // Stack children vertically
                                      overflow         : "auto"                      },

            // Component-specific styles
            "webc-user-files-tree-view": {  //flex             : "1"                         ,            // Take available space
                                            overflowY        : "auto"                      ,            // Scroll if needed
                                            minHeight        : "0"                         },           // Allow content to scroll

            "webc-user-files-actions" : { padding          : "1rem"                 },            // Padding around actions
            "webc-user-files-upload"  : { padding          : "1rem"                 } ,           // Padding around upload

            ".preview-section"     : { flex              : "1"                         ,            // Take available space
                                      minHeight         : "0"                         ,            // Allow content to scroll
                                      overflowY         : "auto"                      },           // Enable scrolling

                ".chat-section"        : { height            : "400px"                     ,            // Fixed height
                                          marginTop         : "1rem"                      ,            // Space above chat
                                          flexShrink        : "0"                         }            // Prevent shrinking

        }
    }
}

WebC__User_Files.define()