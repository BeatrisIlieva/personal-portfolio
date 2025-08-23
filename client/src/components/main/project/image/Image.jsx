import styles from './Image.module.scss';

export const Image = ({ imageName }) => {
    return (
        <article className={styles['thumbnail']}>
            <img src={`/project-media/${imageName}`} alt={imageName} />
        </article>
    );
};
