// WebC__Files__Tree_View.mjs
import Web_Component    from '../../core/Web_Component.mjs'
import CSS__Tree_View   from '../../css/tree_view/CSS__Tree_View.mjs'
import CSS__Icons       from '../../css/icons/CSS__Icons.mjs'
import CSS__Forms       from '../../css/CSS__Forms.mjs'
import Icon             from '../../css/icons/Icon.mjs'
import API__Invoke      from '../../data/API__Invoke.mjs'
import Div              from '../../core/Div.mjs'
import Button           from '../../core/Button.mjs'
import Input            from '../../core/Input.mjs'

export default class WebC__User_Files__Tree_View extends Web_Component {
    load_attributes() {
        new CSS__Tree_View(this).apply_framework()
        new CSS__Icons    (this).apply_framework()
        new CSS__Forms    (this).apply_framework()
        this.api_invoke = new API__Invoke()
        this.data      = null
    }

    async connectedCallback() {
        super.connectedCallback()
        await this.load_data()
        this.render()
        this.add_event_listeners()
    }

    async load_data() {
        try {
            this.data = await this.api_invoke.invoke_api('/api/user-data/files/json-view')
        } catch (error) {
            console.error('Error loading file structure:', error)
            this.data = { node_type: 'folder', children: [], files: [] }
        }
    }

    async add_folder(parentId, folderName) {
        try {
            await this.api_invoke.invoke_api('/api/user-data/files/add-folder', 'POST', {
                folder_name      : folderName,
                parent_folder_id : parentId
            })
            await this.refresh()
        } catch (error) {
            console.error('Error adding folder:', error)
        }
    }

    async refresh() {
        await this.load_data()
        this.render()
        this.add_event_listeners()
    }

    // file_to_base64(file) {
    //     return new Promise((resolve, reject) => {
    //         const reader    = new FileReader()
    //         reader.onload  = () => resolve(reader.result.split(',')[1])
    //         reader.onerror = error => reject(error)
    //         reader.readAsDataURL(file)
    //     })
    // }


    create_tree_item(node, level = 0) {
        if (node === null) { return new Div() }

        const item_div = new Div({ class: 'tree-item', attributes: {
            'data-id': node.node_id,
            'data-type': node.node_type,
            'data-level': level
        }})
        const content  = new Div({ class: `tree-item-content level-${level}` })  // Add level class

        let is_root  = node.parent_id === null
        let expand = is_root || true                                            // expand by default

        if (node.node_type === 'folder') {

            const chevron  = new Icon({ icon: 'chevron-right', class: `tree-item-icon ${node.children?.length ? '' : 'hidden'} ${is_root ? 'tree-item-expanded' : ''}`})
            const folder   = new Icon({ icon: 'folder'       , class: 'tree-item-icon folder-icon'})
            content.add_elements(chevron, folder)

            const children = new Div({class: `tree-children ${expand ? '' : 'tree-folder-closed'}`, id: `folder-${node.node_id}`})

            node.children?.forEach(child => children.add_element(this.create_tree_item(child, level + 1)))
            node.files   ?.forEach(file  => children.add_element(this.create_tree_item(file, level + 1)))

            item_div.add_elements(content, children)
        } else {
            const file_icon = new Icon({ icon: 'file', class: 'tree-item-icon file-icon' })
            content.add_element(file_icon)
            item_div.add_element(content)
        }

        const text    = new Div({ class: 'tree-item-text', value: node.name })
        const actions = new Div({ class: 'tree-item-actions' })

        content.add_elements(text, actions)
        return item_div
    }

    handle__on_click__chevron(item, chevron, event) {
        event.stopPropagation();
        const children = item.querySelector('.tree-children');
        children.classList.toggle('tree-folder-closed');
        chevron.classList.toggle('tree-item-expanded');
    }

    handle__on_click__file(item, event) {
        event.stopPropagation();
        const custom_event = new CustomEvent('file-selected', { detail: { node_id: item.dataset.id,
                                                                          name: item.querySelector('.tree-item-text').textContent },
                                                                          bubbles: true    ,
                                                                          composed: true   })
        this.dispatchEvent(custom_event)
    }

    handle__on_click__folder = (item, event) =>{
        event.stopPropagation()

        this.shadowRoot.querySelectorAll('.tree-item-content.selected').forEach(i => {          // Remove previous selections
            i.classList.remove('selected')
        })

        item.querySelector('.tree-item-content').classList.add('selected')

        // Dispatch selection event
        const custom_event = new CustomEvent('folder-selected', {detail  : {node_id : item.dataset.id,
                                                                            name    : item.querySelector('.tree-item-text').textContent },
                                                                            bubbles : true,
                                                                            composed: true })
        this.dispatchEvent(custom_event)
    }


    add_event_listeners() {
        window.shadow__root = this.shadowRoot
        this.shadowRoot.querySelectorAll('.tree-item').forEach(item => {
            const chevron = item.querySelector('.tree-item-icon');
            if (chevron && !chevron.classList.contains('hidden')) {
                chevron.addEventListener('click', this.handle__on_click__chevron.bind(this, item, chevron));
            }
        });

        this.shadowRoot.querySelectorAll('.tree-item[data-type="folder"]').forEach(item => {
            item.addEventListener('click', this.handle__on_click__folder.bind(this, item));
        })

        this.shadowRoot.querySelectorAll('.tree-item[data-type="file"]').forEach(item => {
            item.addEventListener('click', this.handle__on_click__file.bind(this, item))
        })

    }

    css_rules() {
        return {
            ".tree-add-menu"          : { position         : "absolute",
                                         right            : "0",
                                         top              : "100%",
                                         backgroundColor  : "#fff",
                                         border           : "1px solid #dee2e6",
                                         borderRadius     : "0.25rem",
                                         padding          : "0.5rem",
                                         zIndex           : "1000",
                                         boxShadow        : "0 2px 4px rgba(0,0,0,0.1)"            },

            ".tree-menu-button"       : { display          : "block",
                                         width            : "100%",
                                         padding          : "0.5rem 1rem",
                                         textAlign        : "left",
                                         border           : "none",
                                         backgroundColor  : "transparent",
                                         cursor           : "pointer"                               },

            ".tree-menu-button:hover" : { backgroundColor  : "var(--table-hover-bg)"               },

            ".hidden"                 : { display          : "none"                                 },

            ".tree-view-modal"        : { position         : "fixed",
                                         top              : "50%",
                                         left             : "50%",
                                         transform        : "translate(-50%, -50%)",
                                         backgroundColor  : "#fff",
                                         padding          : "1rem",
                                         borderRadius     : "0.375rem",
                                         boxShadow        : "0 4px 6px rgba(0,0,0,0.1)"           }
        }
    }

    render() {
        const tree = new Div({ class: 'tree-view' })
        tree.add_element(this.create_tree_item(this.data))
        this.set_inner_html(tree.html())
        this.add_css_rules(this.css_rules())
    }
}

WebC__User_Files__Tree_View.define()