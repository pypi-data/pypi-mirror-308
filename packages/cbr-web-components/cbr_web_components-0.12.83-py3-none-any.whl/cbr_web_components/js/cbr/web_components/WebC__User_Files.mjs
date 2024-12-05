// WebC__User_Files.mjs
import Web_Component           from '../../core/Web_Component.mjs'
import Div                     from '../../core/Div.mjs'

export default class WebC__User_Files extends Web_Component {
    load_attributes() {
        this.add_css_rules(this.css_rules())
    }

    connectedCallback() {
        super.connectedCallback()
        this.build()
        this.add_event_listeners()
    }

    add_event_listeners() {
        this.shadowRoot.addEventListener('files-refresh', () => {
            const tree_view = this.shadowRoot.querySelector('webc-user-files-tree-view')
            if (tree_view) {
                tree_view.refresh()
            }
        })
    }

    build() {
        const container = new Div({ class: 'files-container' })

        container.add_tag({ tag: 'webc-user-files-tree-view' })
        container.add_tag({ tag: 'webc-user-files-actions'   })

        this.set_inner_html(container.html())
    }

    css_rules() {
        return {
            ".files-container": { display       : "flex"   ,
                                  flexDirection : "column" ,
                                  gap           : "2rem"   ,
                                  padding       : "1rem"   ,
                                  width         : "100%"   }
        }
    }
}

WebC__User_Files      .define()