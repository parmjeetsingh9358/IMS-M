/** @odoo-module */

const {Component} = owl;

export class ChatterAttachmentsViewer extends Component {}

ChatterAttachmentsViewer.template =
    "mysisco_complain_register.ChatterAttachmentsViewer";
ChatterAttachmentsViewer.props = {
    attachments: Array,
    canDelete: {type: Boolean, optional: true},
    delete: {type: Function, optional: true},
};
ChatterAttachmentsViewer.defaultProps = {
    delete: async () => {},
};
