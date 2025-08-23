import styles from './CircleMatrix.module.scss';

export default function CircleMatrix({ left = '8em', top = '0' }) {
    const rows = 8;
    const cols = 8;
    const cellCount = rows * cols;

    return (
        <div className={styles['matrix-container']} style={{ left, top }}>
            <div
                className={styles['matrix-grid']}
                role='grid'
                aria-rowcount={rows}
                aria-colcount={cols}
            >
                {Array.from({ length: cellCount }).map((_, i) => (
                    <div
                        key={i}
                        className={styles['matrix-circle']}
                        role='gridcell'
                        aria-label={`row ${Math.floor(i / cols) + 1}, column ${
                            (i % cols) + 1
                        }`}
                    />
                ))}
            </div>
        </div>
    );
}
