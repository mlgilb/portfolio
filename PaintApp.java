import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.awt.image.BufferedImage;
import java.util.ArrayList;
import java.util.Random;

public class PaintApp extends JFrame {
    private final DrawingPanel drawingPanel;
    private final JComboBox<String> toolSelector;
    private final JButton colorButton, clearButton;
    private final JSlider thicknessSlider;
    private Color currentColor = Color.BLACK;
    private String currentTool = "Pen";
    private int brushSize = 5;

    public PaintApp() {
        setTitle("Knockoff MS Paint (Advanced)");
        setSize(900, 600);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLayout(new BorderLayout());

        // Drawing area
        drawingPanel = new DrawingPanel();
        add(drawingPanel, BorderLayout.CENTER);

        // Tool Selector
        String[] tools = {"Pen", "Pencil", "Airbrush", "Eraser", "Fill", "Color Dropper"};
        toolSelector = new JComboBox<>(tools);
        toolSelector.addActionListener(e -> currentTool = (String) toolSelector.getSelectedItem());

        // Color Picker
        colorButton = new JButton("Pick Color");
        colorButton.addActionListener(e -> {
            currentColor = JColorChooser.showDialog(this, "Choose a color", currentColor);
            drawingPanel.setColor(currentColor);
        });

        // Brush Thickness Slider
        thicknessSlider = new JSlider(1, 20, 5);
        thicknessSlider.addChangeListener(e -> brushSize = thicknessSlider.getValue());

        // Clear Button
        clearButton = new JButton("Clear");
        clearButton.addActionListener(e -> drawingPanel.clearCanvas());

        // Toolbar Layout
        JPanel controls = new JPanel();
        controls.add(toolSelector);
        controls.add(colorButton);
        controls.add(new JLabel("Brush Size:"));
        controls.add(thicknessSlider);
        controls.add(clearButton);

        add(controls, BorderLayout.NORTH);
    }

    private class DrawingPanel extends JPanel {
        private final BufferedImage canvas;
        private final Graphics2D g2d;
        private int lastX, lastY;
        private final Random random = new Random();

        public DrawingPanel() {
            setBackground(Color.WHITE);
            canvas = new BufferedImage(900, 600, BufferedImage.TYPE_INT_ARGB);
            g2d = canvas.createGraphics();
            g2d.setColor(Color.WHITE);
            g2d.fillRect(0, 0, canvas.getWidth(), canvas.getHeight());

            addMouseListener(new MouseAdapter() {
                @Override
                public void mousePressed(MouseEvent e) {
                    lastX = e.getX();
                    lastY = e.getY();
                    if ("Fill".equals(currentTool)) {
                        floodFill(lastX, lastY, g2d.getColor());
                    } else if ("Color Dropper".equals(currentTool)) {
                        currentColor = new Color(canvas.getRGB(lastX, lastY));
                        colorButton.setBackground(currentColor);
                    }
                }
            });

            addMouseMotionListener(new MouseMotionAdapter() {
                @Override
                public void mouseDragged(MouseEvent e) {
                    int x = e.getX(), y = e.getY();
                    switch (currentTool) {
                        case "Pen" -> drawLine(x, y, brushSize, false);
                        case "Pencil" -> drawLine(x, y, 1, false);
                        case "Eraser" -> drawLine(x, y, brushSize, true);
                        case "Airbrush" -> airBrush(x, y);
                    }
                    lastX = x;
                    lastY = y;
                    repaint();
                }
            });
        }

        private void drawLine(int x, int y, int size, boolean erase) {
            g2d.setColor(erase ? Color.WHITE : currentColor);
            g2d.setStroke(new BasicStroke(size, BasicStroke.CAP_ROUND, BasicStroke.JOIN_ROUND));
            g2d.drawLine(lastX, lastY, x, y);
        }

        private void airBrush(int x, int y) {
            g2d.setColor(currentColor);
            for (int i = 0; i < 30; i++) {
                int dx = random.nextInt(brushSize * 2) - brushSize;
                int dy = random.nextInt(brushSize * 2) - brushSize;
                g2d.fillRect(x + dx, y + dy, 1, 1);
            }
        }

        private void floodFill(int x, int y, Color newColor) {
            int targetColor = canvas.getRGB(x, y);
            if (targetColor == newColor.getRGB()) return;

            ArrayList<Point> queue = new ArrayList<>();
            queue.add(new Point(x, y));

            while (!queue.isEmpty()) {
                Point p = queue.remove(0);
                int px = p.x, py = p.y;

                if (px < 0 || px >= canvas.getWidth() || py < 0 || py >= canvas.getHeight()) continue;
                if (canvas.getRGB(px, py) != targetColor) continue;

                g2d.setColor(newColor);
                g2d.fillRect(px, py, 1, 1);
                canvas.setRGB(px, py, newColor.getRGB());

                queue.add(new Point(px + 1, py));
                queue.add(new Point(px - 1, py));
                queue.add(new Point(px, py + 1));
                queue.add(new Point(px, py - 1));
            }
            repaint();
        }

        public void setColor(Color color) {
            g2d.setColor(color);
        }

        public void clearCanvas() {
            g2d.setColor(Color.WHITE);
            g2d.fillRect(0, 0, canvas.getWidth(), canvas.getHeight());
            repaint();
        }

        @Override
        protected void paintComponent(Graphics g) {
            super.paintComponent(g);
            g.drawImage(canvas, 0, 0, null);
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> new PaintApp().setVisible(true));
    }
}
