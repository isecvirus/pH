package org.virus.ph;

import com.formdev.flatlaf.extras.components.FlatButton;
import com.formdev.flatlaf.intellijthemes.FlatHighContrastIJTheme;
import com.sun.jna.Platform;
import java.awt.Color;
import java.awt.Cursor;
import java.awt.Toolkit;
import java.awt.datatransfer.Clipboard;
import java.awt.datatransfer.StringSelection;
import java.util.ArrayList;
import java.util.EventObject;
import java.util.List;
import javax.swing.Box;
import javax.swing.JButton;
import javax.swing.JComboBox;
import javax.swing.JFileChooser;
import javax.swing.JLabel;
import javax.swing.JMenuItem;
import javax.swing.JOptionPane;
import javax.swing.JPopupMenu;
import javax.swing.JTextField;
import javax.swing.JToggleButton;
import javax.swing.JToolBar;
import javax.swing.RowFilter;
import javax.swing.SwingConstants;
import javax.swing.UIManager;
import javax.swing.UnsupportedLookAndFeelException;
import javax.swing.event.DocumentEvent;
import javax.swing.event.DocumentListener;
import javax.swing.filechooser.FileNameExtensionFilter;
import javax.swing.table.DefaultTableCellRenderer;
import javax.swing.table.DefaultTableModel;
import javax.swing.table.TableRowSorter;
import jiconfont.icons.font_awesome.FontAwesome;
import jiconfont.swing.IconFontSwing;
import org.pcap4j.core.BpfProgram;
import org.pcap4j.core.NotOpenException;
import org.pcap4j.core.PacketListener;
import org.pcap4j.core.PcapHandle;
import org.pcap4j.core.PcapNativeException;
import org.pcap4j.core.PcapNetworkInterface;
import org.pcap4j.core.Pcaps;
import org.pcap4j.packet.Packet;

// SPLASH FROM : https://www.freepik.com/popular-psd
class pH {

    private static Color color(int alpha) {
        return new Color(255, 0, 0, alpha);
    }

    private static PcapNetworkInterface device = null;
    private static PcapHandle handle;
    private static PacketListener listener;
    private static int recieved, captured, dropped;

    public static void main(String[] args) throws PcapNativeException, NotOpenException {
        IconFontSwing.register(FontAwesome.getIconFont());
        try {
            UIManager.setLookAndFeel(new FlatHighContrastIJTheme());
        } catch (UnsupportedLookAndFeelException error) {
            debugger.append("\n" + error.getMessage());
        }

        frame = new javax.swing.JFrame("pH (1.0.0)");

        frame.getRootPane().putClientProperty("JRootPane.titleBarBackground", color(25));
        frame.getRootPane().putClientProperty("JRootPane.titleBarForeground", Color.decode("#808080").brighter());

//        UIManager.put("PasswordField.revealIconColor", color(255));
        UIManager.put("PasswordField.capsLockIconColor", color(139));
        UIManager.put("TextField.selectionBackground", color(100));
        UIManager.put("TextArea.selectionBackground", color(100));

        UIManager.put("ScrollPane.smoothScrolling", true);
        UIManager.put("showButtons", true);

        UIManager.put("ToolBar.dockingBackground", color(190));
        UIManager.put("ToolBar.floatingBackground", color(70));
        UIManager.put("ToolBar.gripColor", color(255));

//        UIManager.put("Button.foreground", Color.decode("#808080"));
        UIManager.put("Button.background", color(50));
        UIManager.put("Button.disabledBackground", color(20));
        UIManager.put("Button.default.background", color(50));
        UIManager.put("Button.hoverBackground", color(35));
        UIManager.put("Button.pressedBackground", color(50));
//        UIManager.put("Button.selectedBackground", color(30));

        UIManager.put("Button.toolbar.hoverBackground", color(25));
        UIManager.put("Button.toolbar.pressedBackground", color(50));

//        UIManager.put("CheckBox.icon.selectedBackground", color(150));
//        UIManager.put("CheckBox.icon.checkmarkColor", color(0));
        UIManager.put("TitlePane.unifiedBackground", true);
        UIManager.put("TitlePane.background", new Color(0, 0, 0));
//        UIManager.put("ToolBar.background", color(50));

        UIManager.put("ToolTip.foreground", Color.decode("#ffffff"));
        UIManager.put("ToolTip.background", Color.decode("#b70000"));

        UIManager.put("Table.selectionForeground", Color.decode("#808080").brighter().brighter());
        UIManager.put("Table.foreground", Color.decode("#808080").brighter());
        UIManager.put("Table.background", new Color(0, 0, 0));
        UIManager.put("TableHeader.background", Color.decode("#b70000").darker());
        UIManager.put("TableHeader.separatorColor", Color.white);
        UIManager.put("TableHeader.bottomSeparatorColor", color(255));
//        UIManager.put("Table.selectionBackground", Color.white);
        UIManager.put("Table.selectionInactiveBackground", new Color(50, 0, 0));
        UIManager.put("Table.gridColor", Color.decode("#420000"));
        UIManager.put("Table.sortIconColor", color(255));
        UIManager.put("TableHeader.sortIconPosition", "left");
        UIManager.put("Table.showHorizontalLines", true);
        UIManager.put("Table.showVerticalLines", false);

        UIManager.put("TitlePane.foreground", color(200));
        UIManager.put("TitlePane.background", color(30)); // shows as #673d01
//        UIManager.put("TitlePane.inactiveBackground", Color.decode("#090700"));

        UIManager.put("TitlePane.borderColor", color(255));

        UIManager.put("Spinner.buttonSeparatorColor", color(100));
        UIManager.put("Component.arc", 5); // roundness of some elements

        UIManager.put("TextComponent.arc", 5); // roundness of some elements
        UIManager.put("JButton.buttonType", "roundRect"); // roundness of some elements

        UIManager.put("TitlePane.closeHoverBackground", color(75));
        UIManager.put("TitlePane.closePressedBackground", color(120));

//        UIManager.put("MenuBar.foreground", Color.lightGray);
        UIManager.put("MenuBar.hoverBackground", color(75));
//        UIManager.put("MenuBar.selectionForeground", Color.decode("#ffffff"));
        UIManager.put("MenuBar.selectionBackground", color(175));
        UIManager.put("MenuBar.underlineSelectionColor", color(175));
        UIManager.put("MenuItem.underlineSelectionColor", color(175));
        UIManager.put("MenuItem.underlineSelectionBackground", color(35));
        UIManager.put("MenuItem.underlineSelectionCheckBackground", color(75));
        UIManager.put("MenuItem.selectionBackground", color(200));
        UIManager.put("CheckBoxMenuItem.icon.checkmarkColor", color(255));
        UIManager.put("Menu.icon.arrowColor", color(255));

        UIManager.put("MenuItem.selectionBackground", color(175));
        UIManager.put("MenuBar.borderColor", color(175));
        UIManager.put("MenuItem.selectionType", "underline");
        UIManager.put("MenuBar.underlineSelectionBackground", color(35));

        UIManager.put("Component.arrowType", "chevron"); // triangle

        UIManager.put("TitlePane.centerTitle", true); // center window title 

        UIManager.put("Button.borderColor", color(50));
        UIManager.put("Button.hoverBorderColor", color(100));
        UIManager.put("Button.toolbar.focusColor", color(150));

        UIManager.put("Component.disabledBorderColor", Color.decode("#222222"));
        UIManager.put("Component.focusedBorderColor", color(150));
        UIManager.put("Component.borderColor", color(100));
        UIManager.put("Component.focusColor", color(50));
        UIManager.put("Component.focusWidth", 2);

        UIManager.put("ToggleButton.toolbar.Background", color(25)); // for toggle buttons
        UIManager.put("ToggleButton.toolbar.hoverBackground", color(50)); // for toggle buttons
        UIManager.put("ToggleButton.toolbar.selectedBackground", color(105)); // for toggle buttons
        UIManager.put("ToggleButton.toolbar.pressedBackground", color(65)); // for toggle buttons

        UIManager.put("Button.focusedBorderColor", color(50));
        UIManager.put("Button.default.focusColor", color(100));

//        UIManager.put("ToolTip.border", BorderFactory.createLineBorder(new Color(254, 152, 1, 100)));
//        UIManager.put("ToolBar.separatorColor", new Color(254, 152, 1, 50));
        UIManager.put("SplitPaneDivider.gripColor", color(127));
        UIManager.put("SplitPaneDivider.oneTouchArrowColor", color(127));
        UIManager.put("SplitPaneDivider.oneTouchHoverArrowColor", color(175));
        UIManager.put("SplitPaneDivider.oneTouchPressedArrowColor", color(255));

        UIManager.put("ToolBar.separatorColor", color(100));

        UIManager.put("ScrollBar.track", color(50));
        UIManager.put("ScrollBar.thumb", color(100));
        UIManager.put("ScrollBar.hoverTrackColor", color(75));
        UIManager.put("ScrollBar.hoverThumbColor", color(150));
        UIManager.put("ScrollBar.hoverButtonBackground", color(50));
        UIManager.put("ScrollBar.pressedButtonBackground", color(150));

        UIManager.put("ScrollBar.trackArc", 0);
        UIManager.put("ScrollBar.thumbArc", 0);
        UIManager.put("ScrollBar.showButtons", true);

        List<String> SearchHistory = new ArrayList<>();
        List<String> filterHistory = new ArrayList<>();
        int snapshotLength = 65536; // bytes
        int readTimeout = 50; // ms

        split_pane = new javax.swing.JSplitPane();
        table_panel = new javax.swing.JPanel();
        table_toolbar = new javax.swing.JToolBar();
        table_scrollpane = new javax.swing.JScrollPane();
        table = new javax.swing.JTable() {
            @Override
            public boolean editCellAt(int row, int column, EventObject e) {
                return false;
            }
        ;
        };
        String[] columns = {"No.", "Timestamp", "Data-Link Type", "Length"};

        DefaultTableModel table_model = new DefaultTableModel(0, columns.length);

        TableRowSorter sorter = new TableRowSorter<>(table_model);
        table.setRowSorter(sorter);
        for (int i = 0; i < columns.length; i++) {
            sorter.setSortable(i, false);
        }

        debugger_panel = new javax.swing.JPanel();
        debugger_scrollpane = new javax.swing.JScrollPane();
        debugger = new javax.swing.JTextArea();
        debugger_toolbar = new javax.swing.JToolBar();
        clear_debugger = new javax.swing.JButton(IconFontSwing.buildIcon(FontAwesome.TRASH, 15, color(180)));
        copy_debugger = new javax.swing.JButton(IconFontSwing.buildIcon(FontAwesome.CLONE, 12, color(180)));

        JTextField capture_to = new JTextField();

        JButton capture_to_pick_path = new JButton(IconFontSwing.buildIcon(FontAwesome.FOLDER_OPEN_O, 13, color(255)));

        capture_to_pick_path.addActionListener(e -> {
            JFileChooser fc = new JFileChooser();
            fc.setDialogTitle("Name and set capture location:");
            FileNameExtensionFilter filter = new FileNameExtensionFilter("Pcap (Packet capture)", "pcap");
            fc.setFileFilter(filter);

            int returnVal = fc.showDialog(frame, "Here!");
            if (returnVal == JFileChooser.APPROVE_OPTION) {
                capture_to.setText(fc.getSelectedFile().getAbsolutePath());
            }

        });

        capture_to.putClientProperty("JTextField.leadingComponent", capture_to_pick_path);
        capture_to.putClientProperty("JTextField.showClearButton", true);
        capture_to.putClientProperty("JTextField.placeholderText", "Packet capture file");

        capture = new JToggleButton(IconFontSwing.buildIcon(FontAwesome.HDD_O, 25, color(255)));
        capture.setBackground(color(35));
        capture.addActionListener(e -> {
            if (capture.isSelected()) {
                capture.setIcon(IconFontSwing.buildIcon(FontAwesome.DOWNLOAD, 22, color(255)));
                capture_to.setEnabled(false);
                capture_to_pick_path.setEnabled(false);
            } else {
                capture.setIcon(IconFontSwing.buildIcon(FontAwesome.HDD_O, 25, color(255)));
                capture_to.setEnabled(true);
                capture_to_pick_path.setEnabled(true);
            }
        });
        table_toolbar.add(capture);
        table_toolbar.add(capture_to);
        JLabel $pcap_lbl = new JLabel(".pcap");
        $pcap_lbl.setForeground(color(255));
        table_toolbar.add($pcap_lbl);
//        table_toolbar.add(capture_toolbar);

        JTextField search_field = new JTextField();
        search_field.putClientProperty("JTextField.placeholderText", "Search..");
        search_field.putClientProperty("JTextField.showClearButton", true);

        JToolBar search_toolbar = new JToolBar();

        FlatButton results_count_label = new FlatButton();

        search_toolbar.addSeparator();
        search_toolbar.add(results_count_label);

        search_field.putClientProperty("JTextField.trailingComponent", search_toolbar);
        search_field.putClientProperty("JTextField.leadingIcon", IconFontSwing.buildIcon(FontAwesome.SEARCH, 15, color(180)));

        JButton searchHistory_btn = new JButton(IconFontSwing.buildIcon(FontAwesome.HISTORY, 15, color(180)));

        search_toolbar.add(searchHistory_btn);

        searchHistory_btn.addActionListener(e -> {
            JPopupMenu popupMenu = new JPopupMenu();

            JMenuItem clear_history = new JMenuItem("Clear History", IconFontSwing.buildIcon(FontAwesome.ERASER, 15, color(180)));
            clear_history.setToolTipText("Clear Search History");
            clear_history.addActionListener(ev -> {
                SearchHistory.clear();
            });
            clear_history.setEnabled((!SearchHistory.isEmpty()));
            popupMenu.add(clear_history);
            if (!SearchHistory.isEmpty()) {
                popupMenu.addSeparator();
            }

            for (int sr = 0; sr < SearchHistory.size(); sr++) { // sr=search result
                String query = SearchHistory.get(sr);
                JMenuItem this_item = new JMenuItem(query);
                this_item.addActionListener(item_al -> {
                    search_field.setText(query);
                });

                popupMenu.add(this_item);
            }
            popupMenu.show(searchHistory_btn, 0, searchHistory_btn.getHeight());
        });

        search_field.getDocument().addDocumentListener(new DocumentListener() {
            public void search(String query) {
                if (query.length() > 0) {
                    try {
                        sorter.setRowFilter(RowFilter.regexFilter(query));
                    } catch (Exception error) {
                        debugger.append("\n" + error.getMessage());
                    }

                    if (!SearchHistory.contains(query)) {
                        SearchHistory.add(query);
                    }
                } else {
                    sorter.setRowFilter(null);
                }

                int results_count = table.getRowCount();
                if (search_field.getText().length() > 0) {
                    results_count_label.setVisible(true);
                    results_count_label.setText(String.valueOf(results_count));
                } else {
                    results_count_label.setText("");
                    results_count_label.setVisible(false);
                }
            }

            @Override
            public void changedUpdate(DocumentEvent e) {
                search(search_field.getText());
            }

            @Override
            public void removeUpdate(DocumentEvent e) {
                search(search_field.getText());
            }

            @Override
            public void insertUpdate(DocumentEvent e) {
                search(search_field.getText());
            }
        });

        table_toolbar.add(search_field);

        JTextField filter_field = new JTextField();
        filter_field.putClientProperty("JTextField.leadingIcon", IconFontSwing.buildIcon(FontAwesome.FILTER, 15, color(180)));
        filter_field.putClientProperty("JTextField.placeholderText", "Filter e.g. \"tcp port 80\"");
        filter_field.putClientProperty("JTextField.showClearButton", true);

        JButton filterHistory_btn = new JButton(IconFontSwing.buildIcon(FontAwesome.HISTORY, 15, color(180)));

        JToolBar filter_toolbar = new JToolBar();
        filter_field.putClientProperty("JTextField.trailingComponent", filter_toolbar);

        filter_toolbar.add(filterHistory_btn);

        filterHistory_btn.addActionListener(e -> {
            JPopupMenu popupMenu = new JPopupMenu();

            JMenuItem clear_history = new JMenuItem("Clear History", IconFontSwing.buildIcon(FontAwesome.ERASER, 15, color(180)));
            clear_history.setToolTipText("Clear Search History");
            clear_history.addActionListener(ev -> {
                filterHistory.clear();
            });
            clear_history.setEnabled((!filterHistory.isEmpty()));
            popupMenu.add(clear_history);
            if (!filterHistory.isEmpty()) {
                popupMenu.addSeparator();
            }

            for (int sr = 0; sr < filterHistory.size(); sr++) { // sr=search result
                String query = filterHistory.get(sr);
                JMenuItem this_item = new JMenuItem(query);
                this_item.addActionListener(item_al -> {
                    filter_field.setText(query);
                });

                popupMenu.add(this_item);
            }
            popupMenu.show(filterHistory_btn, 0, filterHistory_btn.getHeight());
        });

        filter_field.getDocument().addDocumentListener(new DocumentListener() {
            public void search(String filter) throws PcapNativeException, NotOpenException {
                if (filter.length() > 0) {
                    try {
                        handle.setFilter(filter_field.getText(), BpfProgram.BpfCompileMode.OPTIMIZE);
                    } catch (Exception error) {
                        debugger.append("\n" + error.getMessage());
                    }

                    if (!filterHistory.contains(filter)) {
                        filterHistory.add(filter);
                    }
                } else {
                    handle.setFilter("", BpfProgram.BpfCompileMode.OPTIMIZE);
                }
            }

            @Override
            public void changedUpdate(DocumentEvent e) {
                try {
                    search(filter_field.getText());
                } catch (PcapNativeException | NotOpenException error) {
                    debugger.append("\n" + error.getMessage());
                }
            }

            @Override
            public void removeUpdate(DocumentEvent e) {
                try {
                    search(filter_field.getText());
                } catch (PcapNativeException | NotOpenException error) {
                    debugger.append("\n" + error.getMessage());
                }
            }

            @Override
            public void insertUpdate(DocumentEvent e) {
                try {
                    search(filter_field.getText());
                } catch (PcapNativeException | NotOpenException error) {
                    debugger.append("\n" + error.getMessage());
                }
            }
        });

        table_toolbar.add(filter_field);

        table_toolbar.addSeparator();

        JButton captured_counter = new JButton("Captured: -");
        JButton received_counter = new JButton("Received: -");
        JButton dropped_counter = new JButton("Dropped: -");

        table_toolbar.add(captured_counter);
        table_toolbar.add(received_counter);
        table_toolbar.add(dropped_counter);

        table_toolbar.addSeparator();

        auto_scroll = new JToggleButton(IconFontSwing.buildIcon(FontAwesome.LEVEL_DOWN, 15, color(180)));
        auto_scroll.setToolTipText("Auto scroll to the last packet");
        auto_scroll.setSelected(true);
        table_toolbar.add(auto_scroll);

        clear_table = new JButton(IconFontSwing.buildIcon(FontAwesome.TRASH, 15, color(180)));
        clear_table.setToolTipText("Clear captured packets from table");
        table_toolbar.add(clear_table);

        clear_table.addActionListener(e -> {
            for (int i = 0; i < table_model.getRowCount(); i++) {
                table_model.removeRow(i);
            }
            table_model.setRowCount(0);
        });

        frame.setDefaultCloseOperation(javax.swing.WindowConstants.EXIT_ON_CLOSE);

        split_pane.setOneTouchExpandable(true);
//        split_pane.setDividerLocation(580);
        split_pane.setOrientation(javax.swing.JSplitPane.VERTICAL_SPLIT);

        table.setModel(table_model);
        table_scrollpane.setViewportView(table);
        table_model.setColumnIdentifiers(columns);

        DefaultTableCellRenderer renderer = new DefaultTableCellRenderer();
        renderer.setHorizontalAlignment(SwingConstants.CENTER);
        for (int i = 0; i < columns.length; i++) {
            table.getColumnModel().getColumn(i).setCellRenderer(renderer);
        }

        table.getTableHeader().setReorderingAllowed(false);
        table.setSelectionMode(0);
        table.setFocusable(false);
        table.setAutoResizeMode(javax.swing.JTable.AUTO_RESIZE_ALL_COLUMNS);

        javax.swing.GroupLayout table_panelLayout = new javax.swing.GroupLayout(table_panel);
        table_panel.setLayout(table_panelLayout);
        table_panelLayout.setHorizontalGroup(
                table_panelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                        .addComponent(table_scrollpane, javax.swing.GroupLayout.DEFAULT_SIZE, 1306, Short.MAX_VALUE)
                        .addGroup(table_panelLayout.createSequentialGroup()
                                .addContainerGap()
                                .addComponent(table_toolbar, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
        );
        table_panelLayout.setVerticalGroup(
                table_panelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                        .addGroup(table_panelLayout.createSequentialGroup()
                                .addComponent(table_toolbar, javax.swing.GroupLayout.PREFERRED_SIZE, 32, javax.swing.GroupLayout.PREFERRED_SIZE)
                                .addPreferredGap(javax.swing.LayoutStyle.ComponentPlacement.RELATED)
                                .addComponent(table_scrollpane, javax.swing.GroupLayout.DEFAULT_SIZE, 532, Short.MAX_VALUE)
                                .addGap(0, 0, 0))
        );

        split_pane.setTopComponent(table_panel);

        debugger.setColumns(20);
        debugger.setRows(5);
        debugger_scrollpane.setViewportView(debugger);
        debugger.setFocusable(false);
        debugger.setCursor(Cursor.getPredefinedCursor(Cursor.DEFAULT_CURSOR));
        debugger.setWrapStyleWord(true);
        debugger.setLineWrap(true);
        debugger.setForeground(Color.decode("#808080").brighter());
        debugger.setAutoscrolls(true);

        debugger_toolbar.setOrientation(javax.swing.SwingConstants.VERTICAL);
        debugger_toolbar.setRollover(true);
        debugger_toolbar.setFloatable(false);

        clear_debugger.setFocusable(false);
        clear_debugger.setHorizontalTextPosition(javax.swing.SwingConstants.CENTER);
        clear_debugger.setVerticalTextPosition(javax.swing.SwingConstants.BOTTOM);
        debugger_toolbar.add(clear_debugger);
        clear_debugger.addActionListener(e -> {
            debugger.setText("");
        });
        copy_debugger.addActionListener(e -> {
            StringSelection selection = new StringSelection(debugger.getText());
            Clipboard clipboard = Toolkit.getDefaultToolkit().getSystemClipboard();
            clipboard.setContents(selection, selection);
        });

        copy_debugger.setFocusable(false);
        copy_debugger.setHorizontalTextPosition(javax.swing.SwingConstants.CENTER);
        copy_debugger.setVerticalTextPosition(javax.swing.SwingConstants.BOTTOM);
        debugger_toolbar.add(copy_debugger);

        debugger_toolbar.add(Box.createVerticalStrut(100));

        javax.swing.GroupLayout debugger_panelLayout = new javax.swing.GroupLayout(debugger_panel);
        debugger_panel.setLayout(debugger_panelLayout);
        debugger_panelLayout.setHorizontalGroup(
                debugger_panelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                        .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, debugger_panelLayout.createSequentialGroup()
                                .addComponent(debugger_toolbar, javax.swing.GroupLayout.PREFERRED_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.PREFERRED_SIZE)
                                .addGap(4, 4, 4)
                                .addComponent(debugger_scrollpane, javax.swing.GroupLayout.DEFAULT_SIZE, 1253, Short.MAX_VALUE))
        );
        debugger_panelLayout.setVerticalGroup(
                debugger_panelLayout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                        .addComponent(debugger_scrollpane)
                        .addComponent(debugger_toolbar, javax.swing.GroupLayout.DEFAULT_SIZE, javax.swing.GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
        );

        split_pane.setRightComponent(debugger_panel);

        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(frame.getContentPane());
        frame.getContentPane().setLayout(layout);
        layout.setHorizontalGroup(
                layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                        .addGroup(javax.swing.GroupLayout.Alignment.TRAILING, layout.createSequentialGroup()
                                .addContainerGap()
                                .addComponent(split_pane, javax.swing.GroupLayout.DEFAULT_SIZE, 1306, Short.MAX_VALUE)
                                .addContainerGap())
        );
        layout.setVerticalGroup(
                layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
                        .addGroup(layout.createSequentialGroup()
                                .addContainerGap()
                                .addComponent(split_pane)
                                .addContainerGap())
        );

        if (!ifaces().equals(null)) {
            List<PcapNetworkInterface> interfaces = ifaces();
            JComboBox<String> interfaces_cb = new JComboBox<>();
            List<String> interfaces_arr = new ArrayList<String>();

            interfaces.forEach(iface -> {
                String name = iface.getDescription();
                interfaces_cb.add(new JMenuItem(name));
                interfaces_arr.add(name);
            });
            Object selected_iface = JOptionPane.showInputDialog(frame, "Pick an interface:", "Hunt on which interface?", JOptionPane.QUESTION_MESSAGE, IconFontSwing.buildIcon(FontAwesome.SUPERPOWERS, 35, color(180)), interfaces_arr.toArray(), interfaces_arr.toArray()[0]);
            if (selected_iface != null) {
                if (interfaces_arr.contains(selected_iface)) {
                    int index = interfaces_arr.indexOf(selected_iface);
                    device = interfaces.get(index);
                    handle = device.openLive(snapshotLength, PcapNetworkInterface.PromiscuousMode.PROMISCUOUS, readTimeout);

                    new Thread(new Runnable() {
                        @Override
                        public void run() {
                            try {
                                handle.loop(0, (Packet packet) -> {
                                    try {
//                                        captured += handle.getStats().getNumPacketsCaptured();
                                        captured_counter.setText("Captured: " + String.valueOf(handle.getStats().getNumPacketsCaptured()));
                                    } catch (PcapNativeException | NotOpenException error) {
                                        debugger.append("\n" + error.getMessage());
                                    }
                                    if (Platform.isWindows()) {
                                        try {
//                                            recieved += handle.getStats().getNumPacketsReceived();
                                            received_counter.setText("Received: " + String.valueOf(handle.getStats().getNumPacketsReceived()));
                                        } catch (PcapNativeException | NotOpenException error) {
                                            debugger.append("\n" + error.getMessage());
                                        }
                                    }
                                    try {
//                                        dropped += handle.getStats().getNumPacketsDropped();
                                        dropped_counter.setText("Dropped: " + String.valueOf(handle.getStats().getNumPacketsDropped()));
                                    } catch (PcapNativeException | NotOpenException error) {
                                        debugger.append("\n" + error.getMessage());
                                    }

                                    if (capture.isSelected()) {
                                        try {
                                            handle.dumpOpen(capture_to.getText() + ".pcap").dump(packet, handle.getTimestamp());
                                        } catch (NotOpenException | PcapNativeException error) {
                                            debugger.append("\n" + error.getMessage());
                                        }
                                    }
                                    Object[] data = {table_model.getRowCount() + 1, handle.getTimestamp(), handle.getDlt(), handle.getOriginalLength()};
                                    table_model.addRow(data);

                                    if (auto_scroll.isSelected()) {
                                        table.scrollRectToVisible(table.getCellRect(table.getRowCount() - 1, table.getColumnCount(), true));
                                    }
                                });
                            } catch (InterruptedException | PcapNativeException | NotOpenException error) {
                                debugger.append("\n" + error.getMessage());
                            }
                        }
                    }).start();

                    frame.pack();
                    frame.setLocationRelativeTo(null);
                    frame.setVisible(true);
                } else {
                    frame.dispose();
                }
            } else {
                frame.dispose();
            }
        }

    }

    static private javax.swing.JFrame frame;
    static private javax.swing.JButton clear_debugger, copy_debugger, clear_table;
    static private javax.swing.JToggleButton capture, auto_scroll;
    static private javax.swing.JPanel table_panel, debugger_panel;
    static private javax.swing.JScrollPane table_scrollpane, debugger_scrollpane;
    static private javax.swing.JSplitPane split_pane;
    static private javax.swing.JTable table;
    static private javax.swing.JTextArea debugger;
    static private javax.swing.JToolBar debugger_toolbar, table_toolbar;

    private static List<PcapNetworkInterface> ifaces() {
        List<PcapNetworkInterface> devices = null;
        try {
            return devices = Pcaps.findAllDevs();
        } catch (PcapNativeException error) {
            debugger.append("\n" + error.getMessage());
        }
        return devices;
    }
}
