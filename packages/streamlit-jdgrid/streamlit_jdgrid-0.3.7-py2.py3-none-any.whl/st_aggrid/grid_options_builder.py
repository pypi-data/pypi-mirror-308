from collections import defaultdict
import pandas as pd


class GridOptionsBuilder:
    """Builder for gridOptions dictionary"""

    def __init__(self):
        self.__grid_options: defaultdict = defaultdict(dict)
        self.sideBar: dict = dict()

    @staticmethod
    def from_dataframe(dataframe, **default_column_parameters):
        """
        Creates an instance and initilizes it from a dataframe.
        ColumnDefs are created based on dataframe columns and data types.

        :param dataframe: a pandas DataFrame.
        :type dataframe: pd.DataFrame

        :param \*\*default_column_parameters: default column parameters
        :type \*\*default_column_parameters: typing.Dict

        :return: The instance initialized from the dataframe definition.
        :rtype: st_aggrid.GridOptionsBuilder
        """

        # numpy types: 'biufcmMOSUV' https://numpy.org/doc/stable/reference/generated/numpy.dtype.kind.html
        type_mapper = {
            "b": ["textColumn"],
            "i": ["numericColumn", "numberColumnFilter"],
            "u": ["numericColumn", "numberColumnFilter"],
            "f": ["numericColumn", "numberColumnFilter"],
            "c": [],
            "m": ["timedeltaFormat"],
            "M": ["dateColumnFilter", "shortDateTimeFormat"],
            "O": [],
            "S": [],
            "U": [],
            "V": [],
        }

        gb = GridOptionsBuilder()
        gb.configure_default_column(**default_column_parameters)

        if any("." in col for col in dataframe.columns):
            gb.configure_grid_options(suppressFieldDotNotation=True)

        for col_name, col_type in zip(dataframe.columns, dataframe.dtypes):
            gb.configure_column(field=col_name, type=type_mapper.get(col_type.kind, []))

        return gb

    def configure_default_column(
        self,
        min_column_width=5,
        resizable=True,
        filterable=True,
        sortable=True,
        editable=False,
        groupable=False,
        sorteable=None,
        **other_default_column_properties,
    ):
        """Configure default column.

        :param min_column_width: Minimum column width. Defaults to ``100``.
        :type min_column_width: int, optional

        :param resizable: All columns will be resizable. Defaults to ``True``.
        :type resizable: bool, optional

        :param filterable: All columns will be filterable. Defaults to ``True``.
        :type filterable: bool, optional

        :param sortable: All columns will be sortable. Defaults to ``True``.
        :type sortable: bool, optional

        :param sorteable: Backwards compatibility alias for ``sortable``. Overrides sortable if not ``None``.
        :type sorteable: bool, optional

        :param groupable: All columns will be groupable based on row values. Defaults to ``True``.
        :type groupable: bool, optional

        :param editable: All columns will be editable. Defaults to ``True``.
        :type editable: bool, optional

        :param groupable: All columns will be groupable. Defaults to ``True``.
        :type groupable: bool, optional

        :param \*\*other_default_column_properties: Key value pairs that will be merged to defaultColDef dict.
            Check ag-grid documentation.
        :type \*\*other_default_column_properties: typing.Dict, optional
        """
        if sorteable is not None:
            sortable = sorteable

        defaultColDef = {
            "minWidth": min_column_width,
            "editable": editable,
            "filter": filterable,
            "resizable": resizable,
            "sortable": sortable,
        }
        if groupable:
            defaultColDef["enableRowGroup"] = groupable

        if other_default_column_properties:
            defaultColDef = {**defaultColDef, **other_default_column_properties}

        self.__grid_options["defaultColDef"] = defaultColDef

    def configure_auto_height(self, autoHeight=True):
        """
        Makes grid autoheight

        :param autoHeight: enable or disable autoheight. Defaults to ``True``.
        :type autoHeight: bool, optional
        """
        if autoHeight:
            self.configure_grid_options(domLayout="autoHeight")
        else:
            self.configure_grid_options(domLayout="normal")

    def configure_grid_options(self, **props):
        """Merges props to gridOptions

        :param props: props dicts will be merged to gridOptions root.
        :type props: typing.Dict
        """
        self.__grid_options.update(props)

    def configure_columns(self, column_names=[], **props):
        """Batch configures columns. Key-pair values from props dict will be merged
        to colDefs which field property is in column_names list.

        :param column_names: Columns field properties. If any of colDefs matches ``**props`` dict is merged.
            Defaults to ``[]``.
        :type column_names: typing.List, optional

        :param \*\*props: props
        :type \*\*props: typing.Dict
        """
        for k in self.__grid_options["columnDefs"]:
            if k in column_names:
                self.__grid_options["columnDefs"][k].update(props)

    def configure_column(self, field, header_name=None, **other_column_properties):
        """Configures an individual column.
        Check https://www.ag-grid.com/javascript-grid-column-properties/ for more information.


        :param field: field name, usually equals the column header.
        :type field: str

        :param header_name: Header name. Defaults to ``None``.
        :type header_name: str, optional

        :param \*\*other_column_properties: column props
        :type \*\*other_column_properties: typing.Dict
        """
        if not self.__grid_options.get("columnDefs", None):
            self.__grid_options["columnDefs"] = defaultdict(dict)

        colDef = {
            "headerName": field if header_name is None else header_name,
            "field": field,
        }

        if other_column_properties:
            colDef = {**colDef, **other_column_properties}

        self.__grid_options["columnDefs"][field].update(colDef)

    def configure_side_bar(
        self, filters_panel=True, columns_panel=True, defaultToolPanel=""
    ):
        """configures the side panel of ag-grid.
           Side panels are enterprise features, please check www.ag-grid.com

        :param filters_panel: Enable filters side panel. Defaults to ``True``.
        :type filters_panel: (bool, optional

        :param columns_panel: Enable columns side panel. Defaults to ``True``.
        :type columns_panel: bool, optional

        :param defaultToolPanel: The default tool panel that should open when grid renders.
            Either ``"filters"`` or ``"columns"``. If value is blank, panel will start closed (default)
        :type defaultToolPanel: str, optional
        """
        filter_panel = {
            "id": "filters",
            "labelDefault": "Filters",
            "labelKey": "filters",
            "iconKey": "filter",
            "toolPanel": "agFiltersToolPanel",
        }

        columns_panel = {
            "id": "columns",
            "labelDefault": "Columns",
            "labelKey": "columns",
            "iconKey": "columns",
            "toolPanel": "agColumnsToolPanel",
        }

        if filters_panel or columns_panel:
            sideBar = {"toolPanels": [], "defaultToolPanel": defaultToolPanel}

            if filters_panel:
                sideBar["toolPanels"].append(filter_panel)
            if columns_panel:
                sideBar["toolPanels"].append(columns_panel)

            self.__grid_options["sideBar"] = sideBar

    def configure_selection(
        self,
        selection_mode: str = "single",
        use_checkbox: bool = False,
        header_checkbox: bool = False,
        header_checkbox_filtered_only: bool = True,
        pre_select_all_rows: bool = False,
        pre_selected_rows: list = None,
        rowMultiSelectWithClick: bool = False,
        suppressRowDeselection: bool = False,
        suppressRowClickSelection: bool = False,
        groupSelectsChildren: bool = True,
        groupSelectsFiltered: bool = True,
    ):
        """Configure grid selection features

        :param selection_mode: Either ``'single'``, ``'multiple'`` or ``'disabled'``. Defaults to ``'single'``.
        :type selection_mode: str, optional

        :param use_checkbox: Set to ``True`` to have checkbox next to each row.
        :type use_checkbox: bool, optional

        :param header_checkbox: Set to ``True`` to have a checkbox in the header to select all rows.
        :type header_checkbox: bool, optional

        :param header_checkbox_filtered_only: If ``header_checkbox`` is set to ``True``, once the header checkbox is clicked, returned rows depend on this parameter.
            If this is set to ``True``, only filtered (shown) rows will be selected and returned.
            If this is set to ``False``, the whole dataframe (all rows regardless of the applied filter) will be selected and returned.
        :type header_checkbox_filtered_only: bool, optional

        :param pre_selected_rows: Use list of dataframe row iloc index to set corresponding rows as selected state on load. Defaults to ``None``.
        :type pre_selected_rows: list, optional

        :param rowMultiSelectWithClick: If ``False``, user must hold shift to multiselect. Defaults to ``True`` if selection_mode is ``'multiple'``.
        :type rowMultiSelectWithClick: bool, optional

        :param suppressRowDeselection: Set to ``True`` to prevent rows from being deselected if you hold down Ctrl and click the row
            (i.e. once a row is selected, it remains selected until another row is selected in its place).
            By default the grid allows deselection of rows.
            Defaults to ``False``.
        :type suppressRowDeselection: bool, optional

        :param suppressRowClickSelection: Suppress row selection by clicking. Useful for checkbox selection for instance.
            Defaults to ``False``.
        :type suppressRowClickSelection: bool, optional

        :param groupSelectsChildren: When rows are grouped selecting a group select all children.
            Defaults to ``True``.
        :type groupSelectsChildren: bool, optional

        :param groupSelectsFiltered: When a group is selected filtered rows are also selected.
            Defaults to ``True``.
        :type groupSelectsFiltered: bool, optional
        """
        if selection_mode == "disabled":
            self.__grid_options.pop("rowSelection", None)
            self.__grid_options.pop("rowMultiSelectWithClick", None)
            self.__grid_options.pop("suppressRowDeselection", None)
            self.__grid_options.pop("suppressRowClickSelection", None)
            self.__grid_options.pop("groupSelectsChildren", None)
            self.__grid_options.pop("groupSelectsFiltered", None)
            return

        if use_checkbox:
            suppressRowClickSelection = True
            first_key = next(iter(self.__grid_options["columnDefs"].keys()))
            self.__grid_options["columnDefs"][first_key]["checkboxSelection"] = True
            if header_checkbox:
                self.__grid_options["columnDefs"][first_key][
                    "headerCheckboxSelection"
                ] = True
                if header_checkbox_filtered_only:
                    self.__grid_options["columnDefs"][first_key][
                        "headerCheckboxSelectionFilteredOnly"
                    ] = True

        if pre_selected_rows:
            self.__grid_options["preSelectedRows"] = pre_selected_rows

        self.__grid_options["rowSelection"] = selection_mode
        self.__grid_options["rowMultiSelectWithClick"] = rowMultiSelectWithClick
        self.__grid_options["suppressRowDeselection"] = suppressRowDeselection
        self.__grid_options["suppressRowClickSelection"] = suppressRowClickSelection
        self.__grid_options["groupSelectsChildren"] = (
            groupSelectsChildren and selection_mode == "multiple"
        )
        self.__grid_options["groupSelectsFiltered"] = groupSelectsFiltered
        # 'preSelectAllRows' has apparently never worked, and always causes DevTools console errors
        self.__grid_options["preSelectAllRows"] = pre_select_all_rows

    def configure_pagination(
        self, enabled=True, paginationAutoPageSize=True, paginationPageSize=10
    ):
        """Configure grid's pagination features

        :param enabled: Self-explanatory. Defaults to ``True``.
        :type enabled: bool, optional

        :param paginationAutoPageSize: Calculates optimal pagination size based on grid Height. Defaults to ``True``.
        :type paginationAutoPageSize: bool, optional

        :param paginationPageSize: Forces page to have this number of rows per page. Defaults to ``10``.
        :type paginationPageSize: int, optional
        """
        if not enabled:
            self.__grid_options.pop("pagination", None)
            self.__grid_options.pop("paginationAutoPageSize", None)
            self.__grid_options.pop("paginationPageSize", None)
            return

        self.__grid_options["pagination"] = True
        if paginationAutoPageSize:
            self.__grid_options["paginationAutoPageSize"] = paginationAutoPageSize
        else:
            self.__grid_options["paginationPageSize"] = paginationPageSize

    def configure_first_column_as_index(
        self,
        suppressMenu: bool = True,
        headerText: str = "",
        resizable=False,
        sortable=True,
    ):
        """
        Configures the first column definition to look as an index column.

        :param suppressMenu: Suppresses the header menu for the index col. Defaults to ``True``.
        :type suppressMenu: bool, optional

        :param headerText: Header for the index column. Defaults to ``""``.
        :type headerText: str, optional

        :param resizable: Make index column resizable. Defaults to ``False``.
        :type resizable: bool, optional

        :param sortable: Make index column sortable. Defaults to ``True``.
        :type sortable: bool, optional
        """

        index_options = {
            "minWidth": 0,
            "cellStyle": {"color": "white", "background-color": "gray"},
            "pinned": "left",
            "resizable": resizable,
            "sortable": sortable,
            "suppressMovable": True,
            "suppressMenu": suppressMenu,
            "menuTabs": ["filterMenuTab"],
        }
        first_col_def = next(iter(self.__grid_options["columnDefs"]))

        self.configure_column(first_col_def, headerText, **index_options)

    def build(self):
        """Builds the gridOptions dictionary

        :return: a ``dict`` containing the configured grid options
        :rtype: typing.Dict
        """
        self.__grid_options["columnDefs"] = list(
            self.__grid_options["columnDefs"].values()
        )

        return self.__grid_options
