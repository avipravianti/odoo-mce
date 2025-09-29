/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { _t } from "@web/core/l10n/translation";

publicWidget.registry.externalSaleInvoice = publicWidget.Widget.extend({
    selector: "#external_invoice_form",
    events: {
        "change #saleSelect": "_onSaleChange",
        "change #partnerSelect": "_onPartnerChange",
        "click #submitRequestBtn": "_onSubmitRequest",
        "click #downloadInvoiceBtn": "_onDownloadInvoice",
    },

    init: function () {
        this._super.apply(this, arguments);
        this.rpc = this.bindService("rpc");

        // Get data from the global variable
        this.data = window.invoiceRequestData || {};

        this.state = {
            partner: this.data.partner || {},
            sales: this.data.sales || [],
            selectedSale: this.data.preselected_sale_id || "",
            selectedPartner: this.data.has_partner ? this.data.partner.id : false,
            loading: false,
            success: false,
            invoiceId: (this.data.invoice && this.data.invoice.id) || false,
            invoiceState: (this.data.invoice && this.data.invoice.state) || "pending",
            showPartnerSelect: !this.data.has_partner,
            token: this.data.token || "",
        };
    },

    start: function () {
        // Set initial state on the UI
        if (this.state.invoiceId) {
            this.state.success = true;
            this._showSuccess("Invoice has been generated.");
        }

        // If we have a preselected sale ID, set it in the dropdown
        if (this.data.preselected_sale_id) {
            this.state.selectedSale = this.data.preselected_sale_id;
            this.$("#saleSelect").val(this.data.preselected_sale_id);
        }

        return this._super.apply(this, arguments);
    },

    _onSaleChange: function (ev) {
        const saleId = ev.target.value;
        this.state.selectedSale = saleId;

        if (saleId && !this.data.has_partner) {
            // When a sale is selected, also select its partner
            const sale = this.state.sales.find((s) => s.id == saleId);
            if (sale) {
                this.state.selectedPartner = sale.partner.id;
                this.$("#partnerSelect").val(this.state.selectedPartner);
            }
        }
    },

    _onPartnerChange: function (ev) {
        this.state.selectedPartner = ev.target.value;
        // Reset sale selection
        this.state.selectedSale = "";
        this.$("#saleSelect").val("");

        this._updateSaleOptions();
    },

    _updateSaleOptions: function () {
        const filteredSales = this._getFilteredSales();
        const $saleSelect = this.$("#saleSelect");

        // Clear existing options except the first one
        $saleSelect.find("option:not(:first)").remove();

        // Add new options
        filteredSales.forEach((sale) => {
            const optionText =
                sale.name +
                " - " +
                (this.state.showPartnerSelect ? sale.partner.name + " - " : "") +
                sale.date_order +
                " (" +
                sale.amount_total +
                ")";
            $saleSelect.append(
                $("<option>", {
                    value: sale.id,
                    text: optionText,
                })
            );
        });
    },

    _getFilteredSales: function () {
        if (!this.state.selectedPartner) return this.state.sales;
        return this.state.sales.filter((sale) => sale.partner.id == this.state.selectedPartner);
    },

    _showError: function (message) {
        this.$(".alert-danger").remove();
        const $error = $('<div class="alert alert-danger"></div>').text(message);
        this.$("#submitRequestBtn").before($error);
    },

    _showSuccess: function (message) {
        // Hide form elements
        this.$(".form-section").hide();

        // Show success message
        const $success = $('<div class="alert alert-success mb-4"></div>').text(message);
        this.$(".result-section").empty().append($success);

        // Show download button if we have an invoice
        if (this.state.invoiceId) {
            const $downloadBtn = $(
                '<button id="downloadInvoiceBtn" class="btn btn-success">Download Invoice PDF</button>'
            );
            this.$(".result-section").append($downloadBtn);
        } else {
            const $info = $(
                '<div class="alert alert-info">Your invoice request has been submitted and is being processed. Please check back later.</div>'
            );
            this.$(".result-section").append($info);
        }

        this.$(".result-section").removeClass("d-none");
    },

    _onSubmitRequest: async function (ev) {
        ev.preventDefault();

        if (!this.state.selectedSale) {
            this._showError("Please select a sales order");
            return;
        }

        if (!this.state.selectedPartner) {
            this._showError("Please select a customer");
            return;
        }

        this.state.loading = true;
        this.$("#submitRequestBtn").prop("disabled", true).text("Processing...");
        this.$(".alert-danger").remove();

        try {
            const result = await this.rpc("/external/sale-invoice/submit", {
                token: this.state.token,
                partner_id: this.state.selectedPartner,
                sale_id: this.state.selectedSale,
            });

            if (result.error) {
                this._showError(result.error);
            } else {
                this.state.success = true;
                this.state.invoiceId = result.invoice_id;
                this.state.invoiceState = result.state;
                this.state.token = result.token;

                this._showSuccess(result.message || "Invoice request submitted successfully");

                // Redirect to the token URL for persistence
                if (!this.state.token && result.token) {
                    window.location.href = `/external/sale-invoice/${result.token}`;
                }
            }
        } catch (error) {
            this._showError("An error occurred while processing your request");
            console.error(error);
        } finally {
            this.state.loading = false;
            this.$("#submitRequestBtn").prop("disabled", false).text("Request Invoice");
        }
    },

    _onDownloadInvoice: function (ev) {
        ev.preventDefault();
        if (this.state.invoiceId) {
            window.open(`/external/sale-invoice/download/${this.state.invoiceId}`, "_blank");
        }
    },
});

export default { publicWidget };
