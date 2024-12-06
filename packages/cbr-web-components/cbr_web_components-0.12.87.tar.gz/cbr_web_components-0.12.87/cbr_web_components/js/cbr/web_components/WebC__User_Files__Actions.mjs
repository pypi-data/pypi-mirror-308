// WebC__Files__Actions.mjs
import Web_Component from '../../core/Web_Component.mjs'
import CSS__Forms    from '../../css/CSS__Forms.mjs'
import API__Invoke   from '../../data/API__Invoke.mjs'
import Div           from '../../core/Div.mjs'
import Text          from '../../core/Text.mjs'
import Button        from '../../core/Button.mjs'
import Input         from '../../core/Input.mjs'

export default class WebC__User_Files__Actions extends Web_Component {
    load_attributes() {
        new CSS__Forms(this).apply_framework()
        this.api_invoke  = new API__Invoke()
        this.current_folder = {
            node_id : null,
            name    : 'root'
        }
    }

    connectedCallback() {
        super.connectedCallback()
        this.add_event_listeners()
        this.render()
    }

    add_event_listeners() {
        document.addEventListener('folder-selected', (e) => {
            this.current_folder = e.detail
            this.render()
        })
    }

    async add_folder(folder_name) {
        try {
            await this.api_invoke.invoke_api('/api/user-data/files/add-folder', 'POST', {
                folder_name      : folder_name,
                parent_folder_id : this.current_folder.node_id
            })
            //this.input.value = ''
            this.raise_refresh_event()
        } catch (error) {
            console.error('Error adding folder:', error)
        }
    }

    async delete_current_folder() {
        if (!this.current_folder.node_id) {
            alert('Cannot delete root folder')
            return
        }

        if (confirm(`Are you sure you want to delete folder "${this.current_folder.name}"?`)) {
            try {
                const path = `/api/user-data/files/delete-folder?folder_id=${this.current_folder.node_id}`
                await this.api_invoke.invoke_api(path, 'DELETE',)
                this.raise_refresh_event()
            } catch (error) {
                console.error('Error deleting folder:', error)
            }
        }
    }

    raise_refresh_event() {
        const event = new CustomEvent('files-refresh', {
            bubbles : true,
            composed: true
        })
        this.dispatchEvent(event)
    }

    css_rules() {
        return {
            ".actions-container"    : { padding           : "1rem",
                                        backgroundColor   : "#fff",
                                        borderRadius      : "0.375rem",
                                        boxShadow         : "2px 2px 4px rgba(0,0,0,0.2)"      },
            ".current-folder"       : { fontSize          : "0.875rem"  ,
                                        color             : "#6c757d"                        },
            ".folder-info"          : { paddingBottom     : "0.5rem"    ,
                                        display          : "flex"       ,
                                        alignItems       : "center"     ,
                                        gap              : "0.5rem"                         },
            ".folder-info .delete"  : { marginLeft       : "auto"                           },
            ".folder-name"          : { fontWeight        : "600",
                                        color             : "#212529"                        },

            ".actions-form"         : { display          : "flex",
                                        gap              : "0.5rem",
                                        marginBottom     : "1rem"                             },

            ".folder-input"         : { flex             : "1"                              },


            ".action-button"        : { padding          : "0.375rem 0.75rem",
                                      fontSize         : "0.875rem",
                                      fontWeight       : "500",
                                      color            : "#fff",
                                      backgroundColor  : "#0d6efd",
                                      border           : "none",
                                      borderRadius     : "0.375rem",
                                      cursor           : "pointer"                          },

            ".action-button:hover"  : { backgroundColor  : "#0b5ed7"                        },

            ".action-button.delete" : { backgroundColor  : "#dc3545"                        },

            ".action-button.delete:hover": { backgroundColor : "#bb2d3b"                    }
        }
    }

    render() {
        const container            = new Div({ class: 'actions-container' })
        const folder_info          = new Div({ class: 'folder-info' })
        const text__current_folder = new Text({ class: 'current-folder' , value: 'Current Folder: '          })
        const text__folder_name    = new Text({ class: 'folder-name'    , value: this.current_folder.name    })
        const text__folder_id      = new Text({ class: 'folder-id'      , value: this.current_folder.node_id})

        const form__new_folder     = new Div   ({ class       : 'actions-form'          })
        const input                = new Input ({ class       : 'input folder-input'    ,
                                                  placeholder : 'New folder name'       ,
                                                  value       : 'new-folder'            })
        const add_button           = new Button({ class       : 'action-button',  value : 'Add Folder' })

        form__new_folder.add_elements(input, add_button)

        const delete_btn  = new Button({ class : 'action-button delete',    value : 'Delete Current Folder' })
        folder_info.add_elements(text__current_folder, text__folder_name, delete_btn)
        container  .add_elements(form__new_folder, folder_info, text__folder_id)

        this.set_inner_html(container.html())
        this.add_css_rules(this.css_rules())

        this.query_selector('.action-button').addEventListener('click', async () => {                   // Add event listeners after elements are in DOM
            const input = this.query_selector('.folder-input')
            const name = input.value.trim()
            if (name) {
                await this.add_folder(name)
            }
        })

        this.query_selector('.action-button.delete').addEventListener('click', async () => {
            await this.delete_current_folder()
        })
    }
}

WebC__User_Files__Actions.define()