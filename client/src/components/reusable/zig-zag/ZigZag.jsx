import styles from './ZigZag.module.scss';

export const ZigZag = ({ left = '8em', top = '0' }) => {
    return (
        <div className={styles['zig-zag']} style={{ left, top }}>
            <svg
                width='800'
                height='800'
                viewBox='0 0 200 200'
                xmlns='http://www.w3.org/2000/svg'
            >
                <polyline
                    points='50,30 50,60 80,60 80,90 110,90 110,120 140,120 140,150'
                    stroke='white'
                    strokeWidth='3'
                    fill='none'
                />
            </svg>
        </div>
    );
};
