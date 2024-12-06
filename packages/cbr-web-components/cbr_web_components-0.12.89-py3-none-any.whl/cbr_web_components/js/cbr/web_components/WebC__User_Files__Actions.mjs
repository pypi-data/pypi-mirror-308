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
                parent_folder_id : this.current_folder.node_id || ''
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

    async rename_current_folder(new_name) {
        if (!this.current_folder.node_id) {
            alert('Cannot rename root folder')
            return
        }

        try {
            await this.api_invoke.invoke_api('/api/user-data/files/folder-rename', 'POST', {
                folder_id       : this.current_folder.node_id,
                new_folder_name : new_name
            })
            this.raise_refresh_event()
        } catch (error) {
            console.error('Error renaming folder:', error)
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
            ".actions-container"    : { padding           : "1rem"                      ,
                                      backgroundColor   : "#fff"                      ,
                                      borderRadius      : "0.375rem"                  ,
                                      boxShadow         : "2px 2px 4px rgba(0,0,0,0.2)",
                                      display          : "flex"                      ,
                                      flexDirection    : "column"                    ,
                                      gap              : "1rem"                      },

            ".folder-info"          : { paddingBottom     : "0.5rem"                   ,
                                      display           : "flex"                      ,
                                      alignItems        : "center"                    ,
                                      gap               : "0.5rem"                    ,
                                      borderBottom      : "1px solid #dee2e6"         },

            ".current-folder"       : { fontSize          : "0.875rem"                 ,
                                      color             : "#6c757d"                   },

            ".folder-name"          : { fontWeight        : "600"                      ,
                                      color             : "#212529"                   },

            ".actions-form"         : { display          : "flex"                      ,
                                      gap              : "0.5rem"                     },

            ".rename-form"          : { display          : "flex"                      ,
                                      gap              : "0.5rem"                     },

            ".folder-input"         : { flex             : "1"                         },

            ".rename-input"         : { flex             : "1"                         },

            ".action-button"        : { padding          : "0.375rem 0.75rem"         ,
                                      fontSize         : "0.875rem"                  ,
                                      fontWeight       : "500"                       ,
                                      color            : "#fff"                      ,
                                      backgroundColor  : "#0d6efd"                   ,
                                      border           : "none"                      ,
                                      borderRadius     : "0.375rem"                  ,
                                      cursor           : "pointer"                   },

            ".action-button:hover"  : { backgroundColor  : "#0b5ed7"                   },

            ".action-button.rename" : { backgroundColor  : "#198754"                   },

            ".action-button.rename:hover": { backgroundColor : "#146c43"               },

            ".action-button.delete" : { backgroundColor  : "#dc3545"                  ,
                                        marginTop        : "auto"                      },  // Push to bottom

            ".action-button.delete:hover": { backgroundColor : "#bb2d3b"              }
        }
    }

    render() {
        const container            = new Div({ class: 'actions-container' })

        // Current folder info at top
        const folder_info          = new Div({ class: 'folder-info' })
        const text__current_folder = new Text({ class: 'current-folder' , value: 'Current Folder: '       })
        const text__folder_name    = new Text({ class: 'folder-name'    , value: this.current_folder.name })
        folder_info.add_elements(text__current_folder, text__folder_name)

        // Add folder form
        const form__new_folder     = new Div   ({ class       : 'actions-form'          })
        const input                = new Input ({ class       : 'input folder-input'    ,
                                                placeholder : 'New folder name'       ,
                                                value       : 'new-folder'            })
        const add_button           = new Button({ class       : 'action-button',  value : 'Add' })

        form__new_folder.add_elements(input, add_button)

        const show_rename_delete = this.current_folder.node_id && this.current_folder.name !== 'root'
        // Only show rename and delete for non-root folders
        if (show_rename_delete) {
            // Rename folder form
            const form__rename_folder  = new Div   ({ class       : 'rename-form'           })
            const rename_input         = new Input ({ class       : 'input rename-input'    ,
                                                    placeholder : 'New name'              ,
                                                    value       : this.current_folder.name })
            const rename_button        = new Button({ class       : 'action-button rename'  ,
                                                    value        : 'Rename'                })

            form__rename_folder.add_elements(rename_input, rename_button)

            // Delete button at bottom
            const delete_btn = new Button({ class : 'action-button delete', value : 'Delete' })

            container.add_elements(folder_info, form__new_folder, form__rename_folder, delete_btn)
        } else {
            container.add_elements(folder_info, form__new_folder)
        }

        this.set_inner_html(container.html())
        this.add_css_rules(this.css_rules())

        // Add folder event listener
        this.query_selector('.action-button').addEventListener('click', async () => {
            const input = this.query_selector('.folder-input')
            const name = input.value.trim()
            if (name) {
                await this.add_folder(name)
            }
        })

        // Only add these listeners if not root folder
        if (show_rename_delete) {
            // Rename folder event listener
            this.query_selector('.action-button.rename').addEventListener('click', async () => {
                const input = this.query_selector('.rename-input')
                const new_name = input.value.trim()
                if (new_name && new_name !== this.current_folder.name) {
                    await this.rename_current_folder(new_name)
                }
            })

            // Delete folder event listener
            this.query_selector('.action-button.delete').addEventListener('click', async () => {
                await this.delete_current_folder()
            })
        }
    }
}

WebC__User_Files__Actions.define()