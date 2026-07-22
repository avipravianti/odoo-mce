/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Component } from "@odoo/owl";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

// Soal 4.1: komponen Field Widget OWL
export class KelasSummaryOWL extends Component {
    static template = "dev_sekolah.KelasSummaryOWL";
    static props = { ...standardFieldProps };

    // Soal 4.3: dua data dari record aktif via props (this.props.record.data)
    get namaKelas() {
        return this.props.record.data.name || "-";
    }
    get totalKelasSekolah() {
        return this.props.record.data.sekolah_jumlah_kelas ?? 0;
    }
}

registry.category("fields").add("kelas_summary_owl", {
    component: KelasSummaryOWL,
    supportedTypes: ["char"],
});
